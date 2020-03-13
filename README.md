# **ParallelSwapMC**

ParallelSwapMC is a plug-in for HOOMD-Blue, a particle simulation toolkit, that allows parallel Monte Carlo simulation of soft & hard continuous-polydisperse particles on CPUs. In particular, it adds moves which swap either the diameter or positions of the particles. The code is largely based on HOOMD-Blue's [Hard Particle Monte Carlo](https://hoomd-blue.readthedocs.io/en/stable/package-hpmc.html) (HPMC) and [Just-in-Time](https://hoomd-blue.readthedocs.io/en/stable/package-jit.html) (JIT) package 

## **Contents** 

Files that come with this plugin:
 - CMakeLists.txt   : main CMake configuration file for the plugin
 - FindHOOMD.cmake  : script to find a HOOMD-Blue installation to link against
 - README.md        : This file
 - swapmc           : Directory containing C++ and Python source codes that interacts with HOOMD-Blue

## **Installation Instructions**

The following instructions were modified from the example plugin provided by HOOMD-Blue. See https://hoomd-blue.readthedocs.io/en/stable/developer.html for other useful information:

### **Please Read! Check Your HOOMD Installation**
To compile this plugin, you (obviously) need to have HOOMD-Blue installed. However, this plugin depends very crucially on the JIT package, which is not always installed if you follow [the steps in HOOMD-Blue's website](https://hoomd-blue.readthedocs.io/en/stable/installation.html). Thus, successful installation of the plugin requires you to follow additional steps. To check if your HOOMD installation has the JIT package, just try to import it and see if Python gives an error:

```python
import hoomd.jit
```

If JIT is not installed, then you need you would see the following error:

```python
ModuleNotFoundError: No module named 'hoomd.jit'
```

If you see thie error, then you would need re-install HOOMD by compiling from source using the following set of instructions. See also the 'additional hints' section if you're trying to install HOOMD on clusters. 


#### **Installing HOOMD with JIT**
 
The requirements for installing HOOMD with JIT is the same as standard HOOMD, except that you need the following package as REQUIRED:
- [LLVM](https://llvm.org/) 5.0.0 <= x.0.0 <= 9.0.0

Most clusters have LLVM as a module you can load. If not, then you can either ask a cluster administrator to install it on the cluster or [install LLVM yourself](https://releases.llvm.org/). At present, HOOMD with JIT can only be installed with any LLVM version above 5.0.0 **but below 9.0.0**. LLVM's Git repository has LLVM 10.0.0, **which is not compatible with HOOMD-Blue (as of v2.9.0)**. So please, be careful!

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
git clone https://github.com/mandadapu-group/parallel-swap-mc
```

Next, configure your build.
```console
$ cd parallel-swap-mc
$ mkdir build
$ cd build
$ cmake ../ -DENABLE_MPI=ON
```

In this step, CMake will try to find the usual required packages (including LLVM). However, it will also try to find a HOOMD installation. If all goes well, then you should see (as part of cmake's output) the following lines:
```console
-- Python output: /home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd
-- Looking for a HOOMD installation at /home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd
-- Found hoomd installation at /home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd
-- Found HOOMD include directory: /home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/include
-- Found PythonLibs: /home/muhammad/anaconda3/envs/hoomd/lib/libpython3.7m.so
```

Note that plugins can only be built against a hoomd build that has been installed via a package or compiled and then
installed via 'make install'. Plugins can only be built against hoomd when it is built as a shared library.

$ mkdir build

$ cd build

$ cmake /path/to/hoomd-mc-swap/

$ make -j4

$ make install

If hoomd is not in your PATH, you can specify the root using

$ cmake /path/to/hoomd-mc-swap -DHOOMD_ROOT=/path/to/hoomd

where ${HOOMD_ROOT}/bin/hoomd is where the hoomd executable is installed

By default, 'make install' will install the plugin into
${HOOMD_ROOT}
And thus, the plugin loads like any other moduls within hoomd (such as hoomd.md and hoomd.hpmc) 

If hoomd is installed in a system directory (such as via an rpm or deb package), then you can still use plugins.
Delete the 'build' and start over. Set the environment variable HOOMD_PLUGINS_DIR in your .bash_profile
 - export HOOMD_PLUGINS_DIR=${HOME}/hoomd_plugins  # as an example

When running cmake, add -DHOOMD_PLUGINS_DIR=${HOOMD_PLUGINS_DIR} to the options
 - cmake /path/to/plugin_template_cpp -DHOOMD_PLUGINS_DIR=${HOOMD_PLUGINS_DIR}

Now, 'make install' will install the plugins into ${HOOMD_PLUGINS_DIR} and hoomd, when launched, will look there
for the plugins.

## **How to Use ParallelSwapMC**

The plugin can now be used in any hoomd script.
