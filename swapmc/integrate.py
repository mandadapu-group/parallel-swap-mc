# Copyright (c) 2009-2019 The Regents of the University of Michigan
# This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

from hoomd import _hoomd
from hoomd.swapmc import _swapmc
from hoomd.swapmc import data as datswap
from hoomd.integrate import _integrator
import numpy as np
import hoomd
import hoomd.hpmc.integrate #as baseintegrate
import sys

class sph_poly(hoomd.hpmc.integrate.mode_hpmc):
    R""" HPMC integration for polydisperse spheres (2D/3D), supporting swap moves.

    Args:
        seed (int): Random number seed
        d (float): Maximum move displacement, Scalar to set for all types, or a dict containing {type:size} to set by type.
        swap_prob: Probability to perform swap over translational moves.
        nselect (int): The number of trial sweep moves to perform in each cell.
        swap_mode (string): choose whether you want to swap diameters 'diameter' or position 'position'
        df_reject: this is the maximum separation distance between two particles. Larger than this, then swap between the two is always rejected.
        restore_state(bool): Restore internal state from initialization file when True. See :py:class:`mode_hpmc`
                             for a description of what state data restored. (added in version 2.2)

    Hard and soft particle Monte Carlo integration method for (polydisperse) spheres.

    Sphere parameters:

    * *diameter* (**required**) - diameter of the sphere (distance units)
    * *orientable* (**default: False**) - set to True for spheres with orientation (added in version 2.3)
    * *ignore_statistics* (**default: False**) - set to True to disable ignore for statistics tracking
    * *ignore_overlaps* (**default: False**) - set to True to disable overlap checks between this and other types with *ignore_overlaps=True*

    Examples::

        mc = hpmc.integrate.sph_poly(seed=415236)
        mc.shape_param.set('A')
        print('diameter = ', mc.shape_param['A'].diameter)

    """

    def __init__(self, seed, d=0.1, swap_prob=0.2, nselect=1, swap_mode="diameter", soft_mode="hard",dr_reject=np.inf,implicit=False,restore_state=False):
        hoomd.util.print_status_line();

        # initialize base class
        #depletant_mode: Where to place random depletants, either ‘circumsphere’ or ‘overlap_regions’. The swap code doesn't use, but it needs to be there
        #for consistenty with HOOMD-blue's HPMC codebase.
        depletant_mode='circumsphere'
        hoomd.hpmc.integrate.mode_hpmc.__init__(self,implicit, depletant_mode);

        # initialize the reflected c++ class
        self.cpp_integrator = _swapmc.IntegratorHPMCPolydisperseSwap(hoomd.context.current.system_definition, seed);

        # set the default parameters
        hoomd.hpmc.integrate.setD(self.cpp_integrator,d);
        
        # setA method sets the amount orientation perturbation. We don't need it, but it is there for consistency with the rest of HOOMD-Blue's
        #HPMC codebase.
        hoomd.hpmc.integrate.setA(self.cpp_integrator,0.1);

        self.cpp_integrator.setTransProb(1-swap_prob);
        self.cpp_integrator.setSwapMode(swap_mode);
        self.cpp_integrator.setSoftMode(soft_mode);
        self.cpp_integrator.setdrReject(dr_reject);
        self.cpp_integrator.setNSelect(nselect);

        hoomd.context.current.system.setIntegrator(self.cpp_integrator);

        self.initialize_shape_params();

        if implicit:
            self.implicit_required_params=['nR', 'depletant_type']

        if restore_state:
            self.restore_state()

    def initialize_shape_params(self):
        shape_param_type = datswap.__dict__[self.__class__.__name__ + "_params"]; # using the naming convention for convenience.

        # setup the coefficient options
        ntypes = hoomd.context.current.system_definition.getParticleData().getNTypes();
        for i in range(0,ntypes):
            type_name = hoomd.context.current.system_definition.getParticleData().getNameByType(i);
            if not type_name in self.shape_param.keys(): # only add new keys
                self.shape_param.update({ type_name: shape_param_type(self, i) });

        # setup the interaction matrix elements
        ntypes = hoomd.context.current.system_definition.getParticleData().getNTypes();
        for i in range(0,ntypes):
            type_name_i = hoomd.context.current.system_definition.getParticleData().getNameByType(i);
            for j in range(0,ntypes):
                type_name_j = hoomd.context.current.system_definition.getParticleData().getNameByType(j);
                if self.overlap_checks.get(type_name_i, type_name_j) is None: # only add new pairs
                    # by default, perform overlap checks
                    hoomd.util.quiet_status()
                    self.overlap_checks.set(type_name_i, type_name_j, True)
                    hoomd.util.unquiet_status()
    # \internal
    # \brief Format shape parameters for pos file output
    # Do I get scewed up here?????
    def format_param_pos(self, param):
        return 'sphere {0}'.format(0);

    def get_type_shapes(self):
        """Get all the types of shapes in the current simulation.

        Examples:
            The types will be either Sphere or Disk, depending on system dimensionality.

            >>> mc.get_type_shapes()  # in 3D
            [{'type': 'Sphere', 'diameter': 1.0, 'orientable': False}]
            >>> mc.get_type_shapes()  # in 2D
            [{'type': 'Disk', 'diameter': 1.0, 'orientable': False}]

        Returns:
            A list of dictionaries, one for each particle type in the system.
        """
        result = []

        ntypes = hoomd.context.current.system_definition.getParticleData().getNTypes();
        dim = hoomd.context.current.system_definition.getNDimensions()

        for i in range(ntypes):
            typename = hoomd.context.current.system_definition.getParticleData().getNameByType(i);
            shape = self.shape_param.get(typename)
            result.append(dict(type='Point',orientable=shape.orientable));
        
        return result
