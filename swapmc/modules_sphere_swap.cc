// Copyright (c) 2009-2019 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

// Include the defined classes that are to be exported to python
#include "IntegratorHPMCSwap.h"
#include "IntegratorHPMCPolydisperse.h"

#include "ShapePolydisperse.h"

/*
These directives were copied from HOOME-blue module_sphere.cc file
Since I have not checked whether our implementation is compatible with 
these header-file codes, they are turned off for now

#include "AnalyzerSDF.h"
#include "ShapeUnion.h"
#include "IntegratorHPMCMonoImplicit.h"
#include "ComputeFreeVolume.h"

#include <hoomd/hpmc/ExternalField.h>
#include <hoomd/hpmc/ExternalFieldWall.h>
#include <hoomd/hpmc/ExternalFieldLattice.h>
#include <hoomd/hpmc/ExternalFieldComposite.h>
#include "ExternalCallback.h"

#include <hoomd/hpmc/UpdaterExternalFieldWall.h>
#include <hoomd/hpmc/UpdaterRemoveDrift.h>
#include <hoomd/hpmc/UpdaterMuVT.h>
#include "UpdaterMuVTImplicit.h"
#include <hoomd/hpmc/UpdaterClusters.h>
#include "UpdaterClustersImplicit.h"
*/

/*
These directives were copied from HOOME-blue module_sphere.cc file
Since our implementation is not GPU-compatible, they are turned-off for now

#ifdef ENABLE_CUDA
#include "IntegratorHPMCMonoGPU.h"
#include "IntegratorHPMCMonoImplicitGPU.h"
#include "IntegratorHPMCMonoImplicitNewGPU.h"
#include "ComputeFreeVolumeGPU.h"
#endif
*/

namespace py = pybind11;

using namespace hpmc;
using namespace hpmc::detail;

namespace hpmc
{
void export_sph_poly(py::module& m)
    {
    export_IntegratorHPMCPolydisperse< ShapePolydisperse >(m, "IntegratorHPMCPolydisperseSwap");
    
    /*
    //These functions were copied from HOOME-blue module_sphere.cc file
    //Since I have not checked whether our implementation is compatible with 
    //the commented header-file codes from above, they are turned off for now
    
    export_IntegratorHPMCMonoImplicit< ShapeSphere >(m, "IntegratorHPMCMonoImplicitSphere");
    export_ComputeFreeVolume< ShapeSphere >(m, "ComputeFreeVolumeSphere");
    export_AnalyzerSDF< ShapeSphere >(m, "AnalyzerSDFSphere");
    export_UpdaterMuVT< ShapeSphereSwap >(m, "UpdaterMuVTSphereSwap");
    export_UpdaterClusters< ShapeSphereSwap >(m, "UpdaterClustersSphereSwap");
    export_UpdaterClustersImplicit< ShapeSphere,IntegratorHPMCMonoImplicit<ShapeSphere> >(m, "UpdaterClustersImplicitSphere");
    export_UpdaterMuVTImplicit< ShapeSphere, IntegratorHPMCMonoImplicit<ShapeSphere> >(m, "UpdaterMuVTImplicitSphere");

    export_ExternalFieldInterface<ShapeSphereSwap>(m, "ExternalFieldSphereSwap");
    export_LatticeField<ShapeSphereSwap>(m, "ExternalFieldLatticeSphereSwap");
    export_ExternalFieldComposite<ShapeSphereSwap>(m, "ExternalFieldCompositeSphereSwap");
    export_RemoveDriftUpdater<ShapeSphereSwap>(m, "RemoveDriftUpdaterSphereSwap");
    export_ExternalFieldWall<ShapeSphereSwap>(m, "WallSphereSwap");
    export_UpdaterExternalFieldWall<ShapeSphereSwap>(m, "UpdaterExternalFieldWallSphereSwap");
    export_ExternalCallback<ShapeSphereSwap>(m, "ExternalCallbackSphereSwap");

    #ifdef ENABLE_CUDA
    export_IntegratorHPMCMonoGPU< ShapeSphere >(m, "IntegratorHPMCMonoGPUSphere");
    export_IntegratorHPMCMonoImplicitGPU< ShapeSphere >(m, "IntegratorHPMCMonoImplicitGPUSphere");
    export_IntegratorHPMCMonoImplicitNewGPU< ShapeSphere >(m, "IntegratorHPMCMonoImplicitNewGPUSphere");
    export_ComputeFreeVolumeGPU< ShapeSphere >(m, "ComputeFreeVolumeGPUSphere");
    #endif
    */
    
    }
}
