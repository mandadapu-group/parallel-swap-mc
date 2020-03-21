# Install script for directory: /home/muhammad/Softwares/parallel-swap-mc/swapmc

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd")
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

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so"
         RPATH "$ORIGIN/..:$ORIGIN:/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd:/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/hpmc")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc" TYPE SHARED_LIBRARY FILES "/home/muhammad/Softwares/parallel-swap-mc/build/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so")
  if(EXISTS "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so"
         OLD_RPATH "/home/muhammad/Softwares/parallel-swap-mc/build/swapmc:/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd:/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/hpmc:"
         NEW_RPATH "$ORIGIN/..:$ORIGIN:/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd:/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/hpmc")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_swapmc.cpython-37m-x86_64-linux-gnu.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/lib_swapmc_llvm.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/lib_swapmc_llvm.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/lib_swapmc_llvm.so"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/lib_swapmc_llvm.so")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc" TYPE SHARED_LIBRARY FILES "/home/muhammad/Softwares/parallel-swap-mc/build/swapmc/lib_swapmc_llvm.so")
  if(EXISTS "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/lib_swapmc_llvm.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/lib_swapmc_llvm.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/lib_swapmc_llvm.so")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/data.py;/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/__init__.py;/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/_hpmc_swap.py;/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/integrate.py;/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/update.py;/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc/patch.py")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/muhammad/anaconda3/lib/python3.7/site-packages/hoomd/swapmc" TYPE FILE FILES
    "/home/muhammad/Softwares/parallel-swap-mc/swapmc/data.py"
    "/home/muhammad/Softwares/parallel-swap-mc/swapmc/__init__.py"
    "/home/muhammad/Softwares/parallel-swap-mc/swapmc/_hpmc_swap.py"
    "/home/muhammad/Softwares/parallel-swap-mc/swapmc/integrate.py"
    "/home/muhammad/Softwares/parallel-swap-mc/swapmc/update.py"
    "/home/muhammad/Softwares/parallel-swap-mc/swapmc/patch.py"
    )
endif()

