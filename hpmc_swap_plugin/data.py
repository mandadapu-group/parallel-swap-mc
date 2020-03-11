# Copyright (c) 2009-2019 The Regents of the University of Michigan
# This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

""" Shape data structures.
"""

import hoomd
import hoomd.hpmc.data
from hoomd.hpmc_swap_plugin import _hpmc_swap_plugin
import numpy

class sph_poly_params(_hpmc_swap_plugin.sph_poly_param_proxy, hoomd.hpmc.data._param):
    def __init__(self, mc, index):
        #Provide a check to make sure the indexing matches the initial tag??
        _hpmc_swap_plugin.sph_poly_param_proxy.__init__(self, mc.cpp_integrator, index);
        hoomd.hpmc.data._param.__init__(self, mc, index);
        self._keys += ['max_radius', 'min_radius','orientable'];
        self.make_fn = _hpmc_swap_plugin.make_sph_poly_params;
        
    def __str__(self):
        # should we put this in the c++ side?
        return "point particle(maxdiameter = {})".format(max(self.diameters))

    def make_param(self, ignore_statistics=False,orientable=False):
        radii = [];
        for i in range(hoomd.context.current.system_definition.getParticleData().getNGlobal()):
            radii.append(hoomd.context.current.system_definition.getParticleData().getDiameter(i))
        min_radius = min(radii)
        max_radius = max(radii)
        return self.make_fn(ignore_statistics,
                            max_radius, 
                            min_radius,
                            orientable,
                            );
