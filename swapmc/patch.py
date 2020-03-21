# Copyright (c) 2009-2019 The Regents of the University of Michigan
# This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.


from hoomd import _hoomd
#from hoomd.jit import _jit
import hoomd
import tempfile
import shutil
import subprocess
import os

import numpy as np
from hoomd.swapmc import _swapmc as _plugin_patch
#from hoomd.jit import patch

#This python file faciltates the creation of relevant patch energies
#we'll do shifted lennard jones and ludovic's system for now
#let's make different classes for different pair potentials. Of course, we'll let the user defined path energy to be available as well
class lj(object):
    R''' Define the patch energy of a lennard jones particle.

    Args:
        scaledr_cut (float): the scale of cutoff radius relative to particle center to center, beyond which all pair interactions are assumed 0.
        eps (float): uniform energetics
        llvm_ir_fname (str): File name of the llvm IR file to load.
        clang_exec (str): The Clang executable to use

    Patch energies define energetic interactions between pairs of shapes in :py:mod:`hpmc <hoomd.hpmc>` integrators.
    Shapes within a cutoff distance of *r_cut* are potentially interacting and the energy of interaction is a function
    the type and orientation of the particles and the vector pointing from the *i* particle to the *j* particle center.

    The :py:class:`user` patch energy takes C++ code, JIT compiles it at run time and executes the code natively
    in the MC loop at with full performance. It enables researchers to quickly and easily implement custom energetic
    interactions without the need to modify and recompile HOOMD.

    .. rubric:: C++ code

    Supply C++ code to the *code* argument and :py:class:`user` will compile the code and call it to evaluate
    patch energies. Compilation assumes that a recent ``clang`` installation is on your PATH. This is convenient
    when the energy evaluation is simple or needs to be modified in python. More complex code (i.e. code that
    requires auxiliary functions or initialization of static data arrays) should be compiled outside of HOOMD
    and provided via the *llvm_ir_file* input (see below).

    The text provided in *code* is the body of a function with the following signature:

    .. code::

        float eval(const vec3<float>& r_ij,
                   unsigned int type_i,
                   const quat<float>& q_i,
                   float d_i,
                   float charge_i,
                   unsigned int type_j,
                   const quat<float>& q_j,
                   float d_j,
                   float charge_j)

    * ``vec3`` and ``quat`` are defined in HOOMDMath.h.
    * *r_ij* is a vector pointing from the center of particle *i* to the center of particle *j*.
    * *type_i* is the integer type of particle *i*
    * *q_i* is the quaternion orientation of particle *i*
    * *d_i* is the diameter of particle *i*
    * *charge_i* is the charge of particle *i*
    * *type_j* is the integer type of particle *j*
    * *q_j* is the quaternion orientation of particle *j*
    * *d_j* is the diameter of particle *j*
    * *charge_j* is the charge of particle *j*
    * Your code *must* return a value.
    * When \|r_ij\| is greater than *r_cut*, the energy *must* be 0. This *r_cut* is applied between
      the centers of the two particles: compute it accordingly based on the maximum range of the anisotropic
      interaction that you implement.

    Example:

    .. code-block:: python

        square_well = """float rsq = dot(r_ij, r_ij);
                            if (rsq < 1.21f)
                                return -1.0f;
                            else
                                return 0.0f;
                      """
        patch = hoomd.jit.patch.user(mc=mc, r_cut=1.1, code=square_well)

    .. rubric:: LLVM IR code

    You can compile outside of HOOMD and provide a direct link
    to the LLVM IR file in *llvm_ir_file*. A compatible file contains an extern "C" eval function with this signature:

    .. code::

        float eval(const vec3<float>& r_ij,
                   unsigned int type_i,
                   const quat<float>& q_i,
                   float d_i,
                   float charge_i,
                   unsigned int type_j,
                   const quat<float>& q_j,
                   float d_j,
                   float charge_j)

    ``vec3`` and ``quat`` are defined in HOOMDMath.h.

    Compile the file with clang: ``clang -O3 --std=c++11 -DHOOMD_LLVMJIT_BUILD -I /path/to/hoomd/include -S -emit-llvm code.cc`` to produce
    the LLVM IR in ``code.ll``.

    .. versionadded:: 2.3
    '''
    def __init__(self, mc, kT, scaledr_cut, eps, mode='shifted', llvm_ir_file=None, clang_exec=None):
        hoomd.util.print_status_line();
        #there is no need to write your own code. By definition, we're 
        if (mode == 'truncated'):
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j);
                            float rcut  = {}*sigma;
                            if (rsq <= rcut*rcut)
                               {{
                               float eps   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               return 4.0f*eps*r6inv*(r6inv-1.0f);
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(scaledr_cut,eps/kT);
        elif (mode == 'shifted'):
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j);
                            float rcut  = {}*sigma;
                            if (rsq <= rcut*rcut)
                               {{
                               float eps   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               
                               float rsqinv_cut = sigmasq /(rcut*rcut);
                               float r6inv_cut = rsqinv_cut*rsqinv_cut*rsqinv_cut;
                               return 4.0f*eps*(r6inv*(r6inv-1.0f)-r6inv_cut*(r6inv_cut-1.0f));
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(scaledr_cut,eps/kT);
        elif (mode == 'force-shift'):
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j);
                            float rcut  = {}*sigma;
                            if (rsq <= rcut*rcut)
                               {{
                               float eps   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               
                               float rsqinv_cut = sigmasq /(rcut*rcut);
                               float r6inv_cut = rsqinv_cut*rsqinv_cut*rsqinv_cut;
                               return 4.0f*eps*( r6inv*(r6inv-1.0f)-r6inv_cut*(r6inv_cut-1.0f) +6*(sqrtf(rsq)/rcut-1.0f)*r6inv_cut*(2*r6inv_cut-1.0f) );
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(scaledr_cut,eps/kT);
        # check if initialization has occurred
        if hoomd.context.exec_conf is None:
            raise RuntimeError('Error creating Lennard-Jones patch energy, call context.initialize() first');

        # raise an error if this run is on the GPU
        if hoomd.context.exec_conf.isCUDAEnabled():
            hoomd.context.msg.error("Patch energies are not supported on the GPU\n");
            raise RuntimeError("Error initializing patch energy");

        # Find a clang executable if none is provided
        if clang_exec is not None:
            clang = clang_exec;
        else:
            clang = 'clang'

        if code is not None and llvm_ir_file is None:
            llvm_ir = self.compile_user(code, clang)
        else:
            # IR is a text file
            with open(llvm_ir_file,'r') as f:
                llvm_ir = f.read()

        self.compute_name = "patch"
        self.cpp_evaluator = _plugin_patch.PatchEnergyJITCustom(hoomd.context.exec_conf, llvm_ir, scaledr_cut);
        mc.set_PatchEnergyEvaluator(self);

        self.mc = mc
        self.enabled = True
        self.log = False

    def compile_user(self, code, clang_exec, fn=None):
        R'''Helper function to compile the provided code into an executable

        Args:
            code (str): C++ code to compile
            clang_exec (str): The Clang executable to use
            fn (str): If provided, the code will be written to a file.


        .. versionadded:: 2.3
        '''
        cpp_function = """
#include "hoomd/HOOMDMath.h"
#include "hoomd/VectorMath.h"

extern "C"
{
float eval(const vec3<float>& r_ij,
    unsigned int type_i,
    const quat<float>& q_i,
    float d_i,
    float charge_i,
    unsigned int type_j,
    const quat<float>& q_j,
    float d_j,
    float charge_j)
    {
"""
        cpp_function += code
        cpp_function += """
    }
}
"""

        include_path = os.path.dirname(hoomd.__file__) + '/include';
        include_path_source = hoomd._hoomd.__hoomd_source_dir__;

        if clang_exec is not None:
            clang = clang_exec;
        else:
            clang = 'clang';

        if fn is not None:
            cmd = [clang, '-O3', '--std=c++11', '-DHOOMD_LLVMJIT_BUILD', '-I', include_path, '-I', include_path_source, '-S', '-emit-llvm','-x','c++', '-o',fn,'-']
        else:
            cmd = [clang, '-O3', '--std=c++11', '-DHOOMD_LLVMJIT_BUILD', '-I', include_path, '-I', include_path_source, '-S', '-emit-llvm','-x','c++', '-o','-','-']
        p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        # pass C++ function to stdin
        output = p.communicate(cpp_function.encode('utf-8'))
        llvm_ir = output[0].decode()

        f = open("llvm_ir_file",'w')
        f.write(llvm_ir)
        f.close()
        
        if p.returncode != 0:
            hoomd.context.msg.error("Error compiling provided code\n");
            hoomd.context.msg.error("Command "+' '.join(cmd)+"\n");
            hoomd.context.msg.error(output[1].decode()+"\n");
            raise RuntimeError("Error initializing patch energy");

        return llvm_ir

    R''' Disable the patch energy and optionally enable it only for logging

    Args:
        log (bool): If true, only use patch energy as a log quantity

    '''
    def disable(self,log=None):
        hoomd.util.print_status_line();

        if log:
            # enable only for logging purposes
            self.mc.cpp_integrator.disablePatchEnergyLogOnly(log)
            self.log = True
        else:
            # disable completely
            self.mc.cpp_integrator.setPatchEnergy(None);
            self.log = False

        self.enabled = False

    R''' (Re-)Enable the patch energy

    '''
    def enable(self):
        hoomd.util.print_status_line()
        self.mc.cpp_integrator.setPatchEnergy(self.cpp_evaluator);

class softrepulsive(object):
    R''' Define the patch energy of a soft-repulsive particle.
    '''
    def __init__(self, mc, kT, scaledr_cut, eps, mode='shifted', llvm_ir_file=None, clang_exec=None):
        hoomd.util.print_status_line();
        #there is no need to write your own code. By definition, we're 
        if (mode == 'truncated'):
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j);
                            float rcut  = {}*sigma;
                            if (rsq <= rcut*rcut)
                               {{
                               float eps   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               return 4.0f*eps*r6inv*r6inv;
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(scaledr_cut,eps/kT);
        elif (mode == 'shifted'):
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j);
                            float rcut  = {}*sigma;
                            if (rsq <= rcut*rcut)
                               {{
                               float eps   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               
                               float rsqinv_cut = sigmasq /(rcut*rcut);
                               float r6inv_cut = rsqinv_cut*rsqinv_cut*rsqinv_cut;
                               return 4.0f*eps*(r6inv*r6inv-r6inv_cut*r6inv_cut);
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(scaledr_cut,eps/kT);
        elif (mode == 'force-shift'):
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j);
                            float rcut  = {}*sigma;
                            if (rsq <= rcut*rcut)
                               {{
                               float eps   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               
                               float rsqinv_cut = sigmasq /(rcut*rcut);
                               float r6inv_cut = rsqinv_cut*rsqinv_cut*rsqinv_cut;
                               return 4.0f*eps*( r6inv*(r6inv)-r6inv_cut*(r6inv_cut) +6*(sqrtf(rsq)/rcut-1.0f)*r6inv_cut*(2*r6inv_cut) );
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(scaledr_cut,eps/kT);
        # check if initialization has occurred
        if hoomd.context.exec_conf is None:
            raise RuntimeError('Error creating Lennard-Jones patch energy, call context.initialize() first');

        # raise an error if this run is on the GPU
        if hoomd.context.exec_conf.isCUDAEnabled():
            hoomd.context.msg.error("Patch energies are not supported on the GPU\n");
            raise RuntimeError("Error initializing patch energy");

        # Find a clang executable if none is provided
        if clang_exec is not None:
            clang = clang_exec;
        else:
            clang = 'clang'

        if code is not None and llvm_ir_file is None:
            llvm_ir = self.compile_user(code, clang)
        else:
            # IR is a text file
            with open(llvm_ir_file,'r') as f:
                llvm_ir = f.read()

        
        self.compute_name = "patch"
        self.cpp_evaluator = _plugin_patch.PatchEnergyJITCustom(hoomd.context.exec_conf, llvm_ir, scaledr_cut);
        mc.set_PatchEnergyEvaluator(self);

        self.mc = mc
        self.enabled = True
        self.log = False

    def compile_user(self, code, clang_exec, fn=None):
        R'''Helper function to compile the provided code into an executable

        Args:
            code (str): C++ code to compile
            clang_exec (str): The Clang executable to use
            fn (str): If provided, the code will be written to a file.


        .. versionadded:: 2.3
        '''
        cpp_function = """
#include "hoomd/HOOMDMath.h"
#include "hoomd/VectorMath.h"

extern "C"
{
float eval(const vec3<float>& r_ij,
    unsigned int type_i,
    const quat<float>& q_i,
    float d_i,
    float charge_i,
    unsigned int type_j,
    const quat<float>& q_j,
    float d_j,
    float charge_j)
    {
"""
        cpp_function += code
        cpp_function += """
    }
}
"""

        include_path = os.path.dirname(hoomd.__file__) + '/include';
        include_path_source = hoomd._hoomd.__hoomd_source_dir__;

        if clang_exec is not None:
            clang = clang_exec;
        else:
            clang = 'clang';

        if fn is not None:
            cmd = [clang, '-O3', '--std=c++11', '-DHOOMD_LLVMJIT_BUILD', '-I', include_path, '-I', include_path_source, '-S', '-emit-llvm','-x','c++', '-o',fn,'-']
        else:
            cmd = [clang, '-O3', '--std=c++11', '-DHOOMD_LLVMJIT_BUILD', '-I', include_path, '-I', include_path_source, '-S', '-emit-llvm','-x','c++', '-o','-','-']
        p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        # pass C++ function to stdin
        output = p.communicate(cpp_function.encode('utf-8'))
        llvm_ir = output[0].decode()

        f = open("llvm_ir_file",'w')
        f.write(llvm_ir)
        f.close()
        
        if p.returncode != 0:
            hoomd.context.msg.error("Error compiling provided code\n");
            hoomd.context.msg.error("Command "+' '.join(cmd)+"\n");
            hoomd.context.msg.error(output[1].decode()+"\n");
            raise RuntimeError("Error initializing patch energy");

        return llvm_ir

    R''' Disable the patch energy and optionally enable it only for logging

    Args:
        log (bool): If true, only use patch energy as a log quantity

    '''
    def disable(self,log=None):
        hoomd.util.print_status_line();

        if log:
            # enable only for logging purposes
            self.mc.cpp_integrator.disablePatchEnergyLogOnly(log)
            self.log = True
        else:
            # disable completely
            self.mc.cpp_integrator.setPatchEnergy(None);
            self.log = False

        self.enabled = False

    R''' (Re-)Enable the patch energy

    '''
    def enable(self):
        hoomd.util.print_status_line()
        self.mc.cpp_integrator.setPatchEnergy(self.cpp_evaluator);

class ludovic(object):
    R''' Define the patch energy of a polydisperse soft-repulsive
    '''
    def __init__(self, mc, kT, scaledr_cut=1.25, v0=1.0, eps=0.2, model='polydisperse12', llvm_ir_file=None, clang_exec=None):
        hoomd.util.print_status_line();

        if (model == "polydisperse12"):
            a = scaledr_cut
            A = np.array([  [1,a**2,a**4],
                            [0,2*a,4*a**3],
                            [0,2,12*a**2]
                            ])
            b = np.array([-v0/a**12,12*v0/a**13,-156*v0/a**14])
            c = np.linalg.solve(A,b)
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j)*(1-{}*fabs(d_i-d_j) );
                            float rcut  = {}*(sigma);
                            if (rsq <= rcut*rcut)
                               {{
                               float v0   = {};
                               float c0   = {};
                               float c1   = {};
                               float c2   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float _rsq = rsq / sigmasq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               return v0*r6inv*r6inv+c0+c1*_rsq+c2*_rsq*_rsq;
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(eps,scaledr_cut,v0/kT,c[0]/kT,c[1]/kT,c[2]/kT);
        elif (model == "lennardjones"):
            a = scaledr_cut
            A = np.array([  [1,a**2,a**4],
                            [0,2*a,4*a**3],
                            [0,2,12*a**2]
                            ])
            b = np.array([-v0*(1/a**12-1/a**6),v0*(12*v0/a**13-6/a**7),-v0*(156/a**14-42/a**8)])
            c = np.linalg.solve(A,b)
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j)*(1-{}*fabs(d_i-d_j) );
                            float rcut  = {}*(sigma);
                            if (rsq <= rcut*rcut)
                               {{
                               float v0   = {};
                               float c0   = {};
                               float c1   = {};
                               float c2   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float _rsq = rsq / sigmasq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               return v0*(r6inv*r6inv-r6inv)+c0+c1*_rsq+c2*_rsq*_rsq;
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(eps,scaledr_cut,v0/kT,c[0]/kT,c[1]/kT,c[2]/kT);
        elif (model == "polydisperse18"):
            a = scaledr_cut
            A = np.array([  [1,a**2,a**4],
                            [0,2*a,4*a**3],
                            [0,2,12*a**2]
                            ])
            b = np.array([-v0*(1/a**18),(18*v0/a**19),-v0*(342/a**20)])
            c = np.linalg.solve(A,b)
            code = """
                            float rsq = dot(r_ij, r_ij);
                            float sigma  = 0.5*( d_i+d_j)*(1-{}*fabs(d_i-d_j) );
                            float rcut  = {}*(sigma);
                            if (rsq <= rcut*rcut)
                               {{
                               float v0   = {};
                               float c0   = {};
                               float c1   = {};
                               float c2   = {};
                               float sigmasq = sigma*sigma;
                               float rsqinv = sigmasq / rsq;
                               float _rsq = rsq / sigmasq;
                               float r6inv = rsqinv*rsqinv*rsqinv;
                               return v0*(r6inv*r6inv*r6inv)+c0+c1*_rsq+c2*_rsq*_rsq;
                               }}
                            else
                               {{
                               return 0.0f;
                               }}
                          """.format(eps,scaledr_cut,v0/kT,c[0]/kT,c[1]/kT,c[2]/kT);
        else:
            raise RuntimeError('Error creating Polydisperse patch energy. Not one of the available models. Perhaps theres a typo?');

        # check if initialization has occurred
        if hoomd.context.exec_conf is None:
            raise RuntimeError('Error creating Lennard-Jones patch energy, call context.initialize() first');

        # raise an error if this run is on the GPU
        if hoomd.context.exec_conf.isCUDAEnabled():
            hoomd.context.msg.error("Patch energies are not supported on the GPU\n");
            raise RuntimeError("Error initializing patch energy");

        # Find a clang executable if none is provided
        if clang_exec is not None:
            clang = clang_exec;
        else:
            clang = 'clang'

        if code is not None and llvm_ir_file is None:
            llvm_ir = self.compile_user(code, clang)
        else:
            # IR is a text file
            with open(llvm_ir_file,'r') as f:
                llvm_ir = f.read()

        self.compute_name = "patch"
        self.cpp_evaluator = _plugin_patch.PatchEnergyJITCustom(hoomd.context.exec_conf, llvm_ir, scaledr_cut);
        mc.set_PatchEnergyEvaluator(self);

        self.mc = mc
        self.enabled = True
        self.log = False

    def compile_user(self, code, clang_exec, fn=None):
        R'''Helper function to compile the provided code into an executable

        Args:
            code (str): C++ code to compile
            clang_exec (str): The Clang executable to use
            fn (str): If provided, the code will be written to a file.


        .. versionadded:: 2.3
        '''
        cpp_function = """
#include "hoomd/HOOMDMath.h"
#include "hoomd/VectorMath.h"

extern "C"
{
float eval(const vec3<float>& r_ij,
    unsigned int type_i,
    const quat<float>& q_i,
    float d_i,
    float charge_i,
    unsigned int type_j,
    const quat<float>& q_j,
    float d_j,
    float charge_j)
    {
"""
        cpp_function += code
        cpp_function += """
    }
}
"""

        include_path = os.path.dirname(hoomd.__file__) + '/include';
        include_path_source = hoomd._hoomd.__hoomd_source_dir__;

        if clang_exec is not None:
            clang = clang_exec;
        else:
            clang = 'clang';

        if fn is not None:
            cmd = [clang, '-O3', '--std=c++11', '-DHOOMD_LLVMJIT_BUILD', '-I', include_path, '-I', include_path_source, '-S', '-emit-llvm','-x','c++', '-o',fn,'-']
        else:
            cmd = [clang, '-O3', '--std=c++11', '-DHOOMD_LLVMJIT_BUILD', '-I', include_path, '-I', include_path_source, '-S', '-emit-llvm','-x','c++', '-o','-','-']
        p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        # pass C++ function to stdin
        output = p.communicate(cpp_function.encode('utf-8'))
        llvm_ir = output[0].decode()
        
        f = open("llvm_ir_file",'w')
        f.write(llvm_ir)
        f.close()

        if p.returncode != 0:
            hoomd.context.msg.error("Error compiling provided code\n");
            hoomd.context.msg.error("Command "+' '.join(cmd)+"\n");
            hoomd.context.msg.error(output[1].decode()+"\n");
            raise RuntimeError("Error initializing patch energy");

        return llvm_ir

    R''' Disable the patch energy and optionally enable it only for logging

    Args:
        log (bool): If true, only use patch energy as a log quantity

    '''
    def disable(self,log=None):
        hoomd.util.print_status_line();

        if log:
            # enable only for logging purposes
            self.mc.cpp_integrator.disablePatchEnergyLogOnly(log)
            self.log = True
        else:
            # disable completely
            self.mc.cpp_integrator.setPatchEnergy(None);
            self.log = False

        self.enabled = False

    R''' (Re-)Enable the patch energy

    '''
    def enable(self):
        hoomd.util.print_status_line()
        self.mc.cpp_integrator.setPatchEnergy(self.cpp_evaluator);
