// Copyright (c) 2009-2019 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

#include "hoomd/HOOMDMath.h"
#include "hoomd/BoxDim.h"
#include "hoomd/hpmc/HPMCPrecisionSetup.h"
#include "hoomd/VectorMath.h"
#include "hoomd/hpmc/Moves.h"
#include "hoomd/AABB.h"
#include "hoomd/ManagedArray.h"

#include <stdexcept>

#ifndef __SHAPE_POLYDISPERSE_H__
#define __SHAPE_POLYDISPERSE_H__

/*! \file ShapePolydisperse.h
    \brief Defines the sphere shape
*/

// need to declare these class methods with __device__ qualifiers when building in nvcc
// DEVICE is __device__ when included in nvcc and blank when included into the host compiler
#ifdef NVCC
#define DEVICE __device__
#define HOSTDEVICE __host__ __device__
#else
#define DEVICE
#define HOSTDEVICE
#endif

#define SMALL 1e-5

namespace hpmc
{

// put a few misc math functions here as they don't have any better home
namespace detail
    {
    //! helper to call CPU or GPU signbit
    template <class T> HOSTDEVICE inline int signbit(const T& a)
        {
        #ifdef __CUDA_ARCH__
        return ::signbit(a);
        #else
        return std::signbit(a);
        #endif
        }

    template <class T> HOSTDEVICE inline T min(const T& a, const T& b)
        {
        #ifdef __CUDA_ARCH__
        return ::min(a,b);
        #else
        return std::min(a,b);
        #endif
        }

    template <class T> HOSTDEVICE inline T max(const T& a, const T& b)
        {
        #ifdef __CUDA_ARCH__
        return ::max(a,b);
        #else
        return std::max(a,b);
        #endif
        }

    template<class T> HOSTDEVICE inline void swap(T& a, T&b)
        {
        T c;
        c = a;
        a = b;
        b = c;
        }
    }

//! Base class for parameter structure data types
struct param_base
    {
    //! Custom new operator
    static void* operator new(std::size_t sz)
        {
        void *ret = 0;
        int retval = posix_memalign(&ret, 32, sz);
        if (retval != 0)
            {
            throw std::runtime_error("Error allocating aligned memory");
            }

        return ret;
        }

    //! Custom new operator for arrays
    static void* operator new[](std::size_t sz)
        {
        void *ret = 0;
        int retval = posix_memalign(&ret, 32, sz);
        if (retval != 0)
            {
            throw std::runtime_error("Error allocating aligned memory");
            }

        return ret;
        }

    //! Custom delete operator
    static void operator delete(void *ptr)
        {
        free(ptr);
        }

    //! Custom delete operator for arrays
    static void operator delete[](void *ptr)
        {
        free(ptr);
        }

    //! Load dynamic data members into shared memory and increase pointer
    /*! \param ptr Pointer to load data to (will be incremented)
        \param available_bytes Size of remaining shared memory allocation
     */
    HOSTDEVICE void load_shared(char *& ptr,unsigned int &available_bytes) const
        {
        // default implementation does nothing
        }
    };
//! Sphere shape template
/*! ShapePolydisperse implements IntegratorHPMC's shape protocol. It serves at the simplest example of a shape for HPMC

    The parameter defining a sphere is just a single Scalar, the sphere radius.

    \ingroup shape
*/
struct sph_poly_params : param_base
    {
    unsigned int ignore;                //!< Bitwise ignore flag for stats, overlaps. 1 will ignore, 0 will not ignore
                                        //   First bit is ignore overlaps, Second bit is ignore statistics
    bool isOriented;                    //!< Flag to specify whether a sphere has orientation or not. Intended for
     OverlapReal max_radius;// = *max_element(radii.begin(), radii.end());
    OverlapReal min_radius;// = *min_element(radii.begin(), radii.end());
                                       //!  for use with anisotropic/patchy pair potentials.

    #ifdef ENABLE_CUDA
    //! Attach managed memory to CUDA stream
    void attach_to_stream(cudaStream_t stream) const
        {
        // default implementation does nothing
        }
    #endif
    } __attribute__((aligned(32)));

struct ShapePolydisperse
    {
    //! Define the parameter type
    typedef sph_poly_params param_type;

    //! Initialize a shape at a given position
    DEVICE ShapePolydisperse(const quat<Scalar>& _orientation, const param_type& _params)
        : orientation(_orientation), params(_params) {}

    //! Does this shape have an orientation
    DEVICE bool hasOrientation() const
        {
        return params.isOriented;
        }

    //! Ignore flag for acceptance statistics
    DEVICE bool ignoreStatistics() const { return params.ignore; }
    
    //! Get the circumsphere diameter
    DEVICE OverlapReal getMaxCircumsphereDiameter() const
        {
        return params.max_radius*OverlapReal(2.0);
        }
    
    //! Get the circumsphere diameter
    DEVICE OverlapReal getMinCircumsphereDiameter() const
        {
        return params.min_radius*OverlapReal(2.0);
        }

    //! Return the bounding box of the shape in world coordinates
    DEVICE detail::AABB getAABB(const vec3<Scalar>& pos, OverlapReal diameter) const
        {
        //OverlapReal radius = Scalar(0.5)*diameter;
        return detail::AABB(pos, diameter);
        }

    //! Returns true if this shape splits the overlap check over several threads of a warp using threadIdx.x
    HOSTDEVICE static bool isParallel() { return false; }

    quat<Scalar> orientation;    //!< Orientation of the sphere (unused)

    const sph_poly_params &params;        //!< Sphere and ignore flags
    };

//! Check if circumspheres overlap
/*! \param r_ab Vector defining the position of shape b relative to shape a (r_b - r_a)
    \param a first shape
    \param b second shape
    \returns true if the circumspheres of both shapes overlap

    \ingroup shape
*/
DEVICE inline bool check_circumsphere_overlap_plugin(const vec3<Scalar>& r_ab, const OverlapReal& a,
    const OverlapReal &b)
    {
    // for now, always return true
    return true;
    }

//! Sphere-Sphere overlap
/*! \param r_ab Vector defining the position of shape b relative to shape a (r_b - r_a)
    \param a first shape
    \param b second shape
    \param err in/out variable incremented when error conditions occur in the overlap test
    \returns true when *a* and *b* overlap, and false when they are disjoint

    \ingroup shape
*/
DEVICE inline bool test_overlap_plugin(const vec3<Scalar>& r_ab, const OverlapReal& a, const OverlapReal& b, unsigned int& err)
    {
    vec3<OverlapReal> dr(r_ab);

    OverlapReal rsq = dot(dr,dr);

    if (rsq < 0.25*(a + b)*(a + b))
        {
        return true;
        }
    else
        {
        return false;
        }
    }

}; // end namespace hpmc

#undef DEVICE
#undef HOSTDEVICE
#endif //__SHAPE_POLYDISPERSE_H__
