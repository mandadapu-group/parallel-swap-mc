# **ParallelSwapMC**

ParallelSwapMC is a plug-in for HOOMD-Blue, a particle simulation toolkit, that allows parallel Monte Carlo simulation of soft & hard continuous-polydisperse particles on CPUs. In particular, it adds moves which swap either the diameter or positions of the particles. The code is largely based on HOOMD-Blue's [Hard Particle Monte Carlo](https://hoomd-blue.readthedocs.io/en/stable/package-hpmc.html) (HPMC) and [Just-in-Time](https://hoomd-blue.readthedocs.io/en/stable/package-jit.html) (JIT) package.

The plugin is currently under *beta* stage.  

## **Contents** 

Files that come with this plugin:
 - CMakeLists.txt   : main CMake configuration file for the plugin
 - FindHOOMD.cmake  : script to find a HOOMD-Blue installation to link against
 - README.md        : This file
 - swapmc           : Directory containing C++ and Python source codes that interacts with HOOMD-Blue

## **ParallelSwapMC vs. HOOMD-Blue's HPMC**
ParallelSwapMC, like HPMC, essentially acts as an independent Monte Carlo package. In fact, you don't need to load HOOMD-Blue's HPMC to use ParallelSwapMC. However there are key differences that one should be **extremely aware of**:
- *ParallelSwapMC only supports spherical particles:* this reflects the intended application of the plugin, which is to simulate poly-disperse spherical atoms/particles. 
- *ParallelSwapMC only supports particles with hard repulsion or particles with soft interactions, but not both:* this is a feature that will be added in a future release.
- *ParallelSwapMC does not particle multi-labelling:* unlike HPMC, all particles will be labelled the same way. Multi-component systems are introduced by changing specifying particle sizes directly.
- *ParallelSwapMC does not have rotational moves:* all HPMC codes will have, by-default, command to output rotational moves or specify translational/rotational move ratio. This is eliminated in ParallelSwapMC
- *ParallelSwapMC (at present) does not support external field, grand canonical ensemble, or cluster moves:* some of these features (cluster moves in particular) will be added in a future release.

## **Installation Instructions**

Parts of the instructions were modified from the example plugin provided by HOOMD-Blue. See https://hoomd-blue.readthedocs.io/en/stable/developer.html for other useful information:

### **Requirements**
The requirements for installing the plugin is the same as standard HOOMD, except that you need the following package as REQUIRED:
- [LLVM](https://llvm.org/) 5.0.0 <= x.0.0 <= 9.0.0


### **Please Read! Check Your HOOMD Installation**
To compile this plugin, you (obviously) need to have HOOMD-Blue installed. However, this plugin depends very crucially on the JIT package, which is not always installed if you follow [the steps in HOOMD-Blue's website](https://hoomd-blue.readthedocs.io/en/stable/installation.html). Thus, successful installation of the plugin requires you to follow additional steps. To check if your HOOMD installation has the JIT package, just try to import it and see if Python gives an error:

```python
import hoomd.jit
```

If JIT is not installed, then you need you would see the following error:

```python
ModuleNotFoundError: No module named 'hoomd.jit'
```

If you see thie error, then you would need re-install HOOMD by compiling from source and with additional build options.  


### **Installing HOOMD with JIT**

(If JIT is installed, then you don't need this step and skip directly to installing the plugin).

The requirements for installing HOOMD with JIT is the same as standard HOOMD, except that you need the following package as REQUIRED:
- [LLVM](https://llvm.org/) 5.0.0 <= x.0.0 <= 9.0.0

Most clusters have LLVM as a module you can load. If not, then you can either ask a cluster administrator to [install LLVM yourself](https://releases.llvm.org/). At present, HOOMD with JIT can only be installed with any LLVM version above 5.0.0 **but below 9.0.0**. LLVM's Git repository has LLVM 10.0.0, **which is not compatible with HOOMD-Blue (as of v2.9.0)**. So please, be careful!

If you haven't done this already, clone HOOMD-Blue from Git:
```console
$ git clone --recursive https://github.com/glotzerlab/hoomd-blue
```
And yes, you do need need the --resursive option. Now, you need to configure with CMake. First create the build folder. It doesn't matter where, but we will choose the hoomd-blue directory that we've just cloned using Git:
```console
$ cd hoomd-blue
$ mkdir build
$ cd build
```

**Here's the most important part**. You need to include an additional flag onto the cmake command if you want to install JIT also, that flag is 'BUILD_JIT' and 'COPY_HEADERS':
```console
-DBUILD_JIT=ON -DCOPY_HEADERS=ON
``` 

Thus, the cmake command you run looks like this:
```console
$ cmake ../ -DCMAKE_INSTALL_PREFIX=`python3 -c "import site; print(site.getsitepackages()[0])"` -DCMAKE_CXX_FLAGS=-march=native -DCMAKE_C_FLAGS=-march=native -DENABLE_CUDA=ON -DENABLE_MPI=ON -DBUILD_JIT=ON -DCOPY_HEADERS=ON
```

A couple of important notes:
- Obviously, if you want to install to a different directory, just type a different directory -DCMAKE_INSTALL_PREFIX=/path/to/installdirectory
- On HOOMD-Blue's installation page, the BUILD_JIT flag is not documented but, as of v2.9.0, this is still available as part of a valid build option. 

Afterwards, you can compile:
```console
$ make -j4
```
or put -j8, if your cluster/workstation can handle it. To install HOOMD to your install directory:
```console
$ make install
```

### **Installing Plugin**

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

Here's a case example. Suppose that I'm installing the plugin in my personal workstation, where my username is 'yourusername' and the Python environment was Conda's 'base'. If all goes well, then I should see (as part of cmake's output) the following lines:
```console
-- Python output: /home/yourusername/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd
-- Looking for a HOOMD installation at /home/yourusername/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd
-- Found hoomd installation at /home/yourusername/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd
-- Found HOOMD include directory: /home/yourusername/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/include
-- Found PythonLibs: /home/yourusername/anaconda3/envs/hoomd/lib/libpython3.7m.so
```

If not, then the following output could be found:
```console
CMake Error at FindHOOMD.cmake:46 (message):
  Could not find hoomd installation, either set HOOMD_ROOT or set
  PYTHON_EXECUTABLE to a python which can find hoomd
Call Stack (most recent call first):
  CMakeLists.txt:8 (include)
```
if the above message is what you found, then delete the contents of your build folder. Next, re-run cmake with the following build option:
```
$ cmake ../ -DHOOMD_ROOT=/path/to/hoomd
```
where ${HOOMD_ROOT}/bin/hoomd is where the hoomd executable is installed. In the example above /path/to/hoomd is /home/yourusername/anaconda3/envs/hoomd/. 

Finally, you would compile and install the plugin:
```console
$ make -j4 install
```

---
**NOTE**

If hoomd is installed in a system directory (such as via an rpm or deb package), then you can still use plugins. This is not applicable if you follow the instructions we just followed in section **Installning HOOMD with JIT**. For completion, we will also provide instructions for this case. 

First, Delete the contents of your build folder. Set the environment variable HOOMD_PLUGINS_DIR inyour .bash_profile or .bashrc:
```console
export HOOMD_PLUGINS_DIR=${HOME}/hoomd_plugins  # as an example
```
When running cmake, you will add -DHOOMD_PLUGINS_DIR=${HOOMD_PLUGINS_DIR} to the options. Go back to your build folder now, and run:
```console
$ cmake ../ -DHOOMD_PLUGINS_DIR=${HOOMD_PLUGINS_DIR}
```

Now, 'make install' will install the plugins into ${HOOMD_PLUGINS_DIR} and hoomd, when launched, will look there
for the plugins.

---


## **How to Use ParallelSwapMC**

The plugin works like HOOMD-Blue's HPMC, but with more limited features. This means that **you should not import hoomd.hpmc to use the plugin**. 

(More Instructions, coming soon . . .)

## **Developer Notes**

(More notes, coming soon . . .)
