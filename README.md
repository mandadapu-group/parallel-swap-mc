
# **ParallelSwapMC**

ParallelSwapMC is a plug-in for HOOMD-Blue, a particle simulation toolkit, that allows Monte Carlo simulation of soft & hard continuous polydisperse particles on multi-CPUs. In particular, it adds moves which swap either the diameter or positions of the particles. The code is largely based on HOOMD-Blue's [Hard Particle Monte Carlo](https://hoomd-blue.readthedocs.io/en/stable/package-hpmc.html) (HPMC) and [Just-in-Time](https://hoomd-blue.readthedocs.io/en/stable/package-jit.html) (JIT) package.

The plugin is ready to use! For now, this file will be a temporary documentation for the plugin. 

## **Contents** 

Files that come with this plugin:
 - CMakeLists.txt   : main CMake configuration file for the plugin
 - FindHOOMD.cmake  : script to find a HOOMD-Blue installation to link against
 - README.md        : This file
 - swapmc           : Directory containing C++ and Python source codes that interacts with HOOMD-Blue

## **ParallelSwapMC vs. HOOMD-Blue's HPMC**
ParallelSwapMC, like HPMC, essentially acts as an independent Monte Carlo package. You don't need to load HOOMD-Blue's HPMC to use ParallelSwapMC. However, there are key differences that one should be **extremely aware of**:
- *ParallelSwapMC only supports spherical particles:* this reflects the intended application of the plugin, which is to simulate poly-disperse spherical atoms/particles. 
- *ParallelSwapMC (at present) only supports particles with hard repulsion or particles with soft interactions, but not both:* this is a feature that will be added in a future release.
- *ParallelSwapMC does not do particle "multi-labeling":* unlike HPMC, all particles will be labeled the same way. Multi-component systems are introduced by changing specifying particle sizes directly.
- *ParallelSwapMC does not have rotational moves:* all HPMC codes will have, by default, command to output rotational moves or specify translational/rotational move ratio. This is eliminated in ParallelSwapMC in favor of adding swap moves.
- *ParallelSwapMC (at present) does not support external field, grand canonical ensemble, or cluster moves:* some of these features (cluster moves in particular) will be added in a future release.

## **Installation Instructions**

Parts of the instructions were modified from the example plugin provided by HOOMD-Blue. See https://hoomd-blue.readthedocs.io/en/stable/developer.html for other useful information.

### Step 1: **Check Requirements**
The requirements for installing the plugin is the same as standard HOOMD, except that you need the following package as REQUIRED:
- [LLVM](https://llvm.org/) 5.0.0 <= x.0.0 <= 9.0.0


### Step 2: **[PLEASE READ]! Check Your HOOMD Installation**
To compile this plugin, you (obviously) need to have HOOMD-Blue installed. This package has been tested on HOOMD v2.9 as well as v2.8. It is highly likely that it will not work on the upcoming v3.0 since they're including major changes in code organization. 

More importantly, this plugin depends very crucially on their [JIT module](https://hoomd-blue.readthedocs.io/en/stable/package-jit.html), which is not always installed if you follow [the steps in HOOMD-Blue's website](https://hoomd-blue.readthedocs.io/en/stable/installation.html). Thus, the successful installation of the plugin requires you to follow additional steps. To check if your HOOMD installation has the JIT package, just try to import it and see if Python gives an error:

```python
import hoomd.jit
```

If JIT is not installed, then you need you would see the following error:

```python
ModuleNotFoundError: No module named 'hoomd.jit'
```

If you see this error, then you would need to re-install HOOMD by compiling from source and with additional build options.  


### Step 3: **Install HOOMD with JIT**

(If JIT is installed, then you don't need this step and skip directly to installing the plugin).

The requirements for installing HOOMD with JIT is the same as standard HOOMD, except that you need the following package as REQUIRED:
- [LLVM](https://llvm.org/) 5.0.0 <= x.0.0 <= 9.0.0

Most clusters have LLVM as a module you can load. If not, then you can either ask a cluster administrator to [install LLVM](https://releases.llvm.org/) or do it yourself. At present, HOOMD with JIT can only be installed with any LLVM version above 5.0.0 **but below 9.0.0**. LLVM's Git repository has LLVM 10.0.0, **which is not compatible with HOOMD-Blue (as of v2.9.0)**. So please, be careful!

If you haven't done this already, clone HOOMD-Blue from Git:
```console
$ git clone --recursive https://github.com/glotzerlab/hoomd-blue
```
And yes, you do need the --recursive option. Now, you need to configure with CMake. First, create the build folder. It doesn't matter where, but we will choose the hoomd-blue directory that we've just cloned using Git:
```console
$ cd hoomd-blue
$ mkdir build
$ cd build
```

**Here's the most important part**. You need to include an additional flag onto the cmake command if you want to install JIT also, that flag is `BUILD_JIT` and `COPY_HEADERS`:
```console
-DBUILD_JIT=ON -DCOPY_HEADERS=ON
``` 
The `BUILD_JIT` is used so that the JIT module will be compiled just like the rest of  HOOMD's modules. The `COPY_HEADERS`flag will allow us to copy header files to the installation target directory. Building the plugin crucially depends on detecting these header files inside the target directory. 

Thus, the CMake command you run looks like this:
```console
$ cmake ../ -DCMAKE_INSTALL_PREFIX=`python3 -c "import site; print(site.getsitepackages()[0])"` -DCMAKE_CXX_FLAGS=-march=native -DCMAKE_C_FLAGS=-march=native -DENABLE_CUDA=ON -DENABLE_MPI=ON -DBUILD_JIT=ON -DCOPY_HEADERS=ON
```
A couple of important notes:
- If you want to install to a different directory, just type a different directory `-DCMAKE_INSTALL_PREFIX=/path/to/install/directory`
- On HOOMD-Blue's installation page, the BUILD_JIT flag is not documented but, as of v2.9.0, this is still available as part of a valid build option. 

Afterward, you can compile:
```console
$ make -j4
```
Or put `-j8`, if your cluster/workstation can handle it. To install HOOMD to your install directory:
```console
$ make install
```

### Step 4: **Installing Plugin**

Now, you're ready to install ParallelSwapMC. The process is similar to installing HOOMD.  First, git clone the project:
```console
$ git clone https://github.com/mandadapu-group/parallel-swap-mc
```

Next, configure your build.
```console
$ cd parallel-swap-mc
$ mkdir build
$ cd build
$ cmake ../ -DENABLE_MPI=ON
```

In this step, CMake will try to find the usual required packages (including LLVM). However, it will also try to find a HOOMD installation. Check your CMake output! 

Here's a case example. Suppose that I'm installing the plugin in my personal workstation, where my username is `yourusername` and the Python environment was `iluvbase`. If all goes well, then I should see (as part of CMake's output) the following lines:
```console
-- Python output: /home/yourusername/anaconda3/envs/iluvbase/lib/python3.7/site-packages/hoomd
-- Looking for a HOOMD installation at /home/yourusername/anaconda3/envs/iluvbase/lib/python3.7/site-packages/hoomd
-- Found hoomd installation at /home/yourusername/anaconda3/envs/iluvbase/lib/python3.7/site-packages/hoomd
-- Found HOOMD include directory: /home/yourusername/anaconda3/envs/iluvbase/lib/python3.7/site-packages/hoomd/include
-- Found PythonLibs: /home/yourusername/anaconda3/envs/iluvbase/lib/libpython3.7m.so
```

If not, then the following output could be found:
```console
CMake Error at FindHOOMD.cmake:46 (message):
  Could not find hoomd installation, either set HOOMD_ROOT or set
  PYTHON_EXECUTABLE to a python which can find hoomd
Call Stack (most recent call first):
  CMakeLists.txt:8 (include)
```
If the above message is what you found, then delete the contents of your build folder. Next, re-run CMake with the following build option:
```
$ cmake ../ -DENABLE_MPI=ON -DHOOMD_ROOT=/path/to/hoomd
```
where `${HOOMD_ROOT}/bin/hoomd` is where the hoomd executable is installed. In the example above `/path/to/hoomd` is `/home/yourusername/anaconda3/envs/iluvbase/`. 

Finally, you would compile and install the plugin:
```console
$ make -j4 install
```

## Additional Notes

If hoomd is installed in a system directory (such as via an rpm or deb package), then you can still use plugins. This is not applicable if you follow the instructions we just followed in section **Step 3: Install HOOMD with JIT**. For completion, we will also provide instructions for this case. 

First, delete the contents of your build folder. Set the environment variable `HOOMD_PLUGINS_DIR` in your `.bash_profile` or `.bashrc`:
```console
export HOOMD_PLUGINS_DIR=${HOME}/hoomd_plugins  # as an example
```
When running cmake, you will add `-DHOOMD_PLUGINS_DIR=${HOOMD_PLUGINS_DIR}` to the options. Go back to your build folder now, and run:
```console
$ cmake ../ -DENABLE_MPI=ON -DHOOMD_PLUGINS_DIR=${HOOMD_PLUGINS_DIR}
```

Now, `make install'`will install the plugins into `${HOOMD_PLUGINS_DIR}`. When hoomd is launched, it will look into that directory for the plugins.

---


## **Job Scripts with ParallelSwapMC**

The plugin works like HOOMD-Blue's HPMC, but with more limited features (see section **ParallelSwapMC vs. HOOMD-Blue's HPMC**). This means that **you don't have to import hoomd.hpmc to use the plugin**. In fact, running a Monte Carlo simulation with ParallelSwapMC works (practically) the same way as HPMC. 

Below is a sample Python Script to run a continuous polydisperse hard disks system, whose particle size distribution is a uniform distribution: 
```python
import hoomd
import hoomd.swapmc as swap
import numpy as np
from numpy.random import uniform, seed

seed(0)
hoomd.context.initialize("--mode=cpu --notice-level=2");

#Initialize Our Own Configuration using a Snapshot
rho = 1.00
LParticles = 16;
NParticles = LParticles**2
dmax = 1.0
dmin = 0.1

Length = dmax*LParticles
MyBox = hoomd.data.boxdim(L=Length, dimensions=2)
snap = hoomd.data.make_snapshot(N=NParticles, box=MyBox, particle_types=['A'])
snap.particles.types = ['A']

def placePolydisperseOnSquare(snap):
    for i in range(LParticles):
        for j in range(LParticles):
            snap.particles.position[i*LParticles+j,0] = Length*(i/LParticles-0.5)
            snap.particles.position[i*LParticles+j,1] = Length*(j/LParticles-0.5)
            snap.particles.position[i*LParticles+j,2] = 0
            snap.particles.diameter[i*LParticles+j] = uniform(dmin,dmax)

placePolydisperseOnSquare(snap)
system = hoomd.init.read_snapshot(snap);

#Set up the Monte Carlo 'integrator'
mc = swap.integrate.sph_poly(d=0.1, seed=1,swap_prob=0.15,swap_mode='diameter',soft_mode='hard');
mc.shape_param.set('A');
#Add box moves to run in NPT ensemble
boxMC = swap.update.boxmc(mc,betaP=20.0,seed=1)
boxMC.volume(delta=0.76, weight=1.0)
d = hoomd.dump.gsd("dump.gsd", period=100, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(10000);
```

Here's another script for a continuous polydisperse system interacting with a pair potential

```python
import hoomd
import hoomd.swapmc as swap
import numpy as np
from numpy.random import uniform, seed

seed(0)
hoomd.context.initialize("--mode=cpu --notice-level=2");

#Initialize Our Own Configuration using a Snapshot
rho = 1.00
LParticles = 16;
NParticles = LParticles**2
dmax = 1.0
dmin = 0.1

Length = 0.85*LParticles
MyBox = hoomd.data.boxdim(L=Length, dimensions=2)
snap = hoomd.data.make_snapshot(N=NParticles, box=MyBox, particle_types=['A'])
snap.particles.types = ['A']

def placePolydisperseOnSquare(snap):
    for i in range(LParticles):
        for j in range(LParticles):
            snap.particles.position[i*LParticles+j,0] = Length*(i/LParticles-0.5)
            snap.particles.position[i*LParticles+j,1] = Length*(j/LParticles-0.5)
            snap.particles.position[i*LParticles+j,2] = 0
            snap.particles.diameter[i*LParticles+j] = uniform(dmin,dmax)

placePolydisperseOnSquare(snap)
system = hoomd.init.read_snapshot(snap);

#Set up the Monte Carlo 'integrator'
mc = swap.integrate.sph_poly(d=0.2, seed=1,nselect=1,swap_prob=0.2, swap_mode='diameter', soft_mode="soft")
mc.shape_param.set('A');
patch = swap.patch.polydisperse(mc=mc, v0 = 1.0, kT=0.25,scaledr_cut=1.25, eps=1.0, m_expnt = 12, n_expnt=0)
d = hoomd.dump.gsd("dump.gsd", period=100, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(10000);
```

Note that the pair potentials available in this plugin are limited to a particular class where the pair potential is given by:

![equation](https://latex.codecogs.com/gif.latex?%5Cphi%28r/%5Csigma_%7B%5Calpha%20%5Cbeta%7D%29%20%3D%20%5Cbegin%7Bcases%7D%20v_0%20%5Cleft%5B%5Cleft%28%5Cdfrac%7B%5Csigma_%7B%5Calpha%20%5Cbeta%7D%7D%7Br%7D%5Cright%29%5Em-%5Cleft%28%5Cdfrac%7B%5Csigma_%7B%5Calpha%20%5Cbeta%7D%7D%7Br%7D%5Cright%29%5En%5Cright%5D&plus;%5Csum_%7Bk%3D0%7D%5Eq%20c_k%20%5Cleft%28%5Cfrac%7Br%5E%7B%5Calpha%20%5Cbeta%7D%7D%7B%5Csigma_%7B%5Calpha%20%5Cbeta%7D%7D%20%5Cright%20%29%5E%7B2k%7D%26%20r/%5Csigma_%7B%5Calpha%20%5Cbeta%7D%20%5Cleq%20%5Ctilde%7Br%7D_c%20%5C%5C%200%20%26%20%5Ctext%7Botherwise%7D%20%5Cend%7Bcases%7D)

![equation](https://latex.codecogs.com/gif.latex?%5Csigma_%7B%5Calpha%20%5Cbeta%7D%20%3D%20%5Cfrac%7B1%7D%7B2%7D%5Cleft%28%5Csigma_%5Calpha%20&plus;%5Csigma_%5Cbeta%5Cright%29%281-%5Cvarepsilon%7C%5Csigma_%5Calpha%20-%20%5Csigma_%5Cbeta%7C%29)

The first term in the first equation is the standard repulsive and attractive interaction. The second term is an even polynomial ensuring smoothness up to q-th order at the cut off radius. The `hoomd.swapmc.patch.polydisperse` class only supports 2nd order continuity!  

You will see in parallel-swap-mc/patch.py file that there are other pair potentials, but I haven't thoroughly tested them or haven't checked their implementation in a long time! So be please be aware. 

## **Developer Notes**

(More notes, coming soon . . .)
