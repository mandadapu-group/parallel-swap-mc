#include "ShapePolydisperse.h" // check
#include <hoomd/managed_allocator.h>
#include <hoomd/extern/gsd.h>
#include <hoomd/GSDDumpWriter.h>
#include <hoomd/GSDReader.h>
#include <hoomd/HOOMDMPI.h>

#include <string>
#include <memory>
#include <stdexcept>
#include <algorithm>
#include <numeric>

#ifndef _GSD_HPMC_Schema_H_
#define _GSD_HPMC_Schema_H_
/*
#include "ShapeConvexPolygon.h" // check
#include "ShapeSpheropolygon.h" // check
#include "ShapePolyhedron.h"
#include "ShapeConvexPolyhedron.h" // check
#include "ShapeSpheropolyhedron.h" // check
#include "ShapeSimplePolygon.h" // check
#include "ShapeEllipsoid.h" // check
#include "ShapeFacetedEllipsoid.h"
#include "ShapeSphinx.h"
#include "ShapeUnion.h"
*/

template<class T>
using param_array = typename std::vector<T, managed_allocator<T> >;

struct gsd_schema_hpmc_base
    {
    gsd_schema_hpmc_base(const std::shared_ptr<const ExecutionConfiguration> exec_conf, bool mpi) : m_exec_conf(exec_conf), m_mpi(mpi) {}
    const std::shared_ptr<const ExecutionConfiguration> m_exec_conf;
    bool m_mpi;
    };

struct gsd_schema_hpmc : public gsd_schema_hpmc_base
    {
    gsd_schema_hpmc(const std::shared_ptr<const ExecutionConfiguration> exec_conf, bool mpi) : gsd_schema_hpmc_base(exec_conf, mpi) {}
    template<class T>
    int write(gsd_handle& handle, const std::string& name, unsigned int Ntypes, const T* const data, gsd_type type)
        {
        if(!m_exec_conf->isRoot())
            return 0;
        int retval = 0;
        retval |= gsd_write_chunk(&handle, name.c_str(), type, Ntypes, 1, 0, (void *)data);
        return retval;
        }

    template<class T>
    bool read(std::shared_ptr<GSDReader> reader, uint64_t frame, const std::string& name, unsigned int Ntypes, T* const data, gsd_type type)
        {
        bool success = true;
        std::vector<T> d;
        if(m_exec_conf->isRoot())
            {
            d.resize(Ntypes);
            success = reader->readChunk((void *) &d[0], frame, name.c_str(), Ntypes*gsd_sizeof_type(type), Ntypes) && success;
            }
    #ifdef ENABLE_MPI
        if(m_mpi)
            {
            bcast(d, 0, m_exec_conf->getMPICommunicator()); // broadcast the data
            }
    #endif
        if(!d.size())
            throw std::runtime_error("Error occurred while attempting to restore from gsd file.");
        for(unsigned int i = 0; i < Ntypes; i++)
            {
            data[i] = d[i];
            }
        return success;
        }
    };

template<class T>
struct gsd_shape_schema : public gsd_schema_hpmc_base
    {
    gsd_shape_schema(const std::shared_ptr<const ExecutionConfiguration> exec_conf, bool mpi) : gsd_schema_hpmc_base(exec_conf, mpi) {}

    int write(gsd_handle&, const std::string&, unsigned int, const param_array<T>& )
        {
        throw std::runtime_error("This is not implemented");
        return 0;
        }
    bool read(std::shared_ptr<GSDReader>, uint64_t, const std::string&, unsigned int, param_array<T>&)
        {
        throw std::runtime_error("This is not implemented");
        return false;
        }
    };

template<>
struct gsd_shape_schema<hpmc::sph_poly_params>: public gsd_schema_hpmc_base
    {
    gsd_shape_schema(const std::shared_ptr<const ExecutionConfiguration> exec_conf, bool mpi) : gsd_schema_hpmc_base(exec_conf, mpi) {}

    int write(gsd_handle& handle, const std::string& name, unsigned int Ntypes, const param_array<hpmc::sph_poly_params>& shape)
        {
        if(!m_exec_conf->isRoot())
            return 0;
        int retval = 0;
        std::string path = name + "radius";
        std::string path_o = name + "orientable";
        std::vector<float> data(Ntypes);
        std::vector<uint8_t> orientableflag(Ntypes);
        //std::transform(shape.begin(), shape.end(), data.begin(), [](const hpmc::sph_poly_params& s)->float{return 0;});
        retval |= gsd_write_chunk(&handle, path.c_str(), GSD_TYPE_FLOAT, Ntypes, 1, 0, (void *)&data[0]);
        std::transform(shape.begin(), shape.end(), orientableflag.begin(), [](const hpmc::sph_poly_params& s)->uint32_t{return s.isOriented;});
        retval |= gsd_write_chunk(&handle, path_o.c_str(), GSD_TYPE_UINT8, Ntypes, 1, 0, (void *)&orientableflag[0]);
        return retval;
        }

    void read(  std::shared_ptr<GSDReader> reader,
                uint64_t frame,
                const std::string& name,
                unsigned int Ntypes,
                param_array<hpmc::sph_poly_params>& shape
            )
        {

        std::string path_o = name + "orientable";
        std::vector<float> data;
        std::string path = name + "radius";
        std::vector<uint8_t> orientableflag(Ntypes);
        bool state_read = true;
        if(m_exec_conf->isRoot())
            {
            data.resize(Ntypes, 0.0);
            orientableflag.resize(Ntypes);
            if(!reader->readChunk((void *) &data[0], frame, path.c_str(), Ntypes*gsd_sizeof_type(GSD_TYPE_FLOAT), Ntypes))
                state_read = false;
            if (reader->getHandle().header.schema_version <= gsd_make_version(1,2))
                {
                std::fill(orientableflag.begin(), orientableflag.end(), 0);
                }
            else if (!reader->readChunk((void *) &orientableflag[0], frame, path_o.c_str(), Ntypes*gsd_sizeof_type(GSD_TYPE_UINT8), Ntypes))
                {
                state_read = false;
                }
            }

        #ifdef ENABLE_MPI
            if(m_mpi)
            {
            bcast(state_read, 0, m_exec_conf->getMPICommunicator());
            bcast(data, 0, m_exec_conf->getMPICommunicator()); // broadcast the data
            bcast(orientableflag, 0, m_exec_conf->getMPICommunicator());
            }
        #endif

        if (!state_read)
            throw std::runtime_error("Error occurred while attempting to restore from gsd file.");

        for(unsigned int i = 0; i < Ntypes; i++)
            {
            //shape[i].radius = data[i];
            shape[i].isOriented = orientableflag[i];
            shape[i].ignore = 0;
            }
        }
    };


#endif
