// Copyright (c) 2009-2019 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

// Include the defined classes that are to be exported to python
//#include <hoomd/hpmc/IntegratorHPMC.h>
//#include <hoomd/hpmc/IntegratorHPMCMono.h>
#include "PatchEnergyJITCustom.h"
#include "PatchEnergyPolydisperse12.h"
//#include "IntegratorHPMCMonoSwap.h"
#include "IntegratorHPMCPolydisperse.h"
//#include <hoomd/hpmc/UpdaterClusters.h>

//#include <hoomd/hpmc/ShapeSphere.h>
#include "ShapePolydisperse.h"
//#include <hoomd/hpmc/ShapeProxy.h>
#include "ShapeProxySwap.h"
#include "UpdaterBoxMCSwap.h"

//#include <hoomd/hpmc/GPUTree.h>

/*
#ifdef ENABLE_CUDA
#include "IntegratorHPMCMonoGPU.h"
#endif
*/

#include "modules_swap.h"

/*! \file module.cc
    \brief Export classes to python
*/
using namespace hpmc; 
using namespace std;
namespace py = pybind11;

namespace hpmc
{

//! HPMC implementation details
/*! The detail namespace contains classes and functions that are not part of the HPMC public interface. These are
    subject to change without notice and are designed solely for internal use within HPMC.
*/
namespace detail
{

// could move the make_param functions back??

}; // end namespace detail

}; // end namespace hpmc

using namespace hpmc::detail;

//! Define the _hpmc python module exports
PYBIND11_MODULE(_swapmc, m)
    {
    export_IntegratorHPMCSwap(m);
    //export_IntegratorHPMCTest(m);
    export_UpdaterBoxMCSwap(m);
    //export_external_fields(m);
    export_sph_poly_params(m);
    //export_shapetest_params(m);
    export_PatchEnergyJITCustom(m);
    export_PatchEnergyPolydisperse12(m);

    //export_point(m);
    export_sph_poly(m);

    py::class_<sph_poly_params, std::shared_ptr<sph_poly_params> >(m, "sph_poly_params", py::module_local());

    m.def("make_sph_poly_params", &make_sph_poly_params);
    m.def("make_overlapreal3", &make_overlapreal3);
    m.def("make_overlapreal4", &make_overlapreal4);

    // export counters
    //export_hpmc_implicit_counters(m); //<< check if this is part of mono or monoimplicit
    //export_hpmc_clusters_counters(m);
    }

/*! \defgroup hpmc_integrators HPMC integrators
*/

/*! \defgroup hpmc_analyzers HPMC analyzers
*/

/*! \defgroup shape Shapes
    Shape classes define the geometry of shapes and associated overlap checks
*/

/*! \defgroup vecmath Vector Math
    Vector, matrix, and quaternion math routines
*/

/*! \defgroup hpmc_detail Details
    HPMC implementation details
    @{
*/

/*! \defgroup hpmc_data_structs Data structures
    HPMC internal data structures
*/

/*! \defgroup hpmc_kernels HPMC kernels
    HPMC GPU kernels
*/

/*! \defgroup minkowski Minkowski methods
    Classes and functions related to Minkowski overlap detection methods
*/

/*! \defgroup overlap Other overlap methods
    Classes and functions related to other (brute force) overlap methods
*/

/*! @} */
