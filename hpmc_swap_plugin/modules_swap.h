// Copyright (c) 2009-2019 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

#ifndef __MODULES_SWAP__
#define __MODULES_SWAP__

#ifndef NVCC
#include <hoomd/extern/pybind/include/pybind11/pybind11.h>
#endif

namespace hpmc
{

    void export_sph_poly(pybind11::module& m);
    void export_external_fields(pybind11::module& m);
}

#endif // __MODULES_SWAP__
