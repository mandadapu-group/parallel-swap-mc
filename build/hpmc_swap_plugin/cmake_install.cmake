# Install script for directory: /media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/hpmc_swap_plugin

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so"
         RPATH "$ORIGIN/..:$ORIGIN:/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd:/usr/local/cuda/lib64:/usr/lib/openmpi/lib:/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc:/home/muhammad/anaconda3/envs/hoomd/lib")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin" TYPE SHARED_LIBRARY FILES "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/build/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so")
  if(EXISTS "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so"
         OLD_RPATH "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/build/hpmc_swap_plugin:/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd:/usr/local/cuda/lib64:/usr/lib/openmpi/lib:/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc:/home/muhammad/anaconda3/envs/hoomd/lib:"
         NEW_RPATH "$ORIGIN/..:$ORIGIN:/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd:/usr/local/cuda/lib64:/usr/lib/openmpi/lib:/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc:/home/muhammad/anaconda3/envs/hoomd/lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap_plugin.cpython-37m-x86_64-linux-gnu.so")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  if(EXISTS "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so"
         RPATH "/home/muhammad/anaconda3/envs/hoomd/lib")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin" TYPE SHARED_LIBRARY FILES "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/build/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so")
  if(EXISTS "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so"
         OLD_RPATH "/home/muhammad/anaconda3/envs/hoomd/lib:"
         NEW_RPATH "/home/muhammad/anaconda3/envs/hoomd/lib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/lib_hpmc_swap_plugin_llvm.so")
    endif()
  endif()
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/data.py;/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/__init__.py;/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/_hpmc_swap.py;/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/integrate.py;/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/update.py;/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin/patch.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/muhammad/anaconda3/envs/hoomd/lib/python3.7/site-packages/hoomd/hpmc_swap_plugin" TYPE FILE FILES
    "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/hpmc_swap_plugin/data.py"
    "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/hpmc_swap_plugin/__init__.py"
    "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/hpmc_swap_plugin/_hpmc_swap.py"
    "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/hpmc_swap_plugin/integrate.py"
    "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/hpmc_swap_plugin/update.py"
    "/media/muhammad/ExtraDrive11/hoomd-blue/other-swap-plugin/hpmc_swap_plugin/patch.py"
    )
endif()

