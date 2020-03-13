# *ParallelSwapMC* - A HOOMD-Blue Plugin for Parallel SWAP Algorithm

ParallelSwapMC is a plug-in for HOOMD-Blue, a particle simulation toolkit, that allows parallel Monte Carlo simulation of soft & hard continuous-polydisperse particles on CPUs. In particular, it adds moves which swap either the diameter or positions of the particles. The code is largely based on HOOMD-Blue's [Hard Particle Monte Carlo](https://hoomd-blue.readthedocs.io/en/stable/package-hpmc.html) (HPMC) and Just-in-Time (JIT) package  

Files that come with this plugin:
 - CMakeLists.txt   : main CMake configuration file for the plugin
 - FindHOOMD.cmake  : script to find a HOOMD-Blue installation to link against
 - README.md           : This file
 - hpmc_swap_plugin    : Directory containing C++ and Python source codes that interacts with HOOMD

The following instructions were modified from the example plugin provided by HOOMD-Blue. See https://hoomd-blue.readthedocs.io/en/stable/developer.html for other useful information:

To compile this plugin, follow steps similar to those in compiling HOOMD-Blue. The process of finding a HOOMD 
installation to link to will be fully automatic IF you have hoomd_install_dir/bin in your PATH when running ccmake.

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

The plugin can now be used in any hoomd script.
