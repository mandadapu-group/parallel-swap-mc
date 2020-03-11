set(COMPONENT_NAME swapmc)

# find and configure LLVM
find_package(LLVM REQUIRED CONFIG)
message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")
message(STATUS "LLVM Definitions: ${LLVM_DEFINITIONS}")
include_directories(${LLVM_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})
llvm_map_components_to_libnames(llvm_libs executionengine support core irreader native runtimedyld orcjit object transformutils lto)


# set the appropriate compiler flags on the _llvm target

set(_${COMPONENT_NAME}_sources 
                    UpdaterBoxMCSwap.cc  
                    IntegratorHPMCSwap.cc 
                    PatchEnergyJITCustom.cc 
                    modules_swap.cc
                    modules_sphere_swap.cc
                    #module-jit-custom.cc
                    )

# we compile a separate package just for the LLVM-interfacing part,
# so that can be compiled with and without RTTI
set(_${COMPONENT_NAME}_llvm_sources EvalFactory.cc)

set(_${COMPONENT_NAME}_headers
                    UpdaterBoxMCSwap.h
                    HPMCCountersSwap.h  
                    IntegratorHPMCSwap.h  
                    IntegratorHPMCMonoSwap.h
                    IntegratorHPMCPolydisperse.h  
                    modules_swap.h  
                    ShapeProxySwap.h  
                    ShapeProxyTest.h
                    ShapePoint.h
                    ShapeSphereSwap.h  
                    PatchEnergyJITCustom.h
                    )

                
pybind11_add_module(_${COMPONENT_NAME} SHARED ${_${COMPONENT_NAME}_sources} NO_EXTRAS)
add_library (_${COMPONENT_NAME}_llvm SHARED ${_${COMPONENT_NAME}_llvm_sources})

list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(AddLLVM)
llvm_update_compile_flags(_${COMPONENT_NAME}_llvm)

# bug: llvm_update_compile_flags removes the c++11 compile flag that hoomd sets for old cmake versions
# cmake 3.1 and newer are not affected becuase we use CMAKE_CXX_STANDARD
if (CMAKE_VERSION VERSION_LESS 3.1.0)
    message(FATAL_ERROR "CMake 3.1.0 or newer is required to buid the JIT module")
endif()

# work around missing LLVM link information
if(LLVM_ENABLE_TERMINFO)
    find_library(TERMINFO NAMES tinfo ncurses)
    if (${TERMINFO} STREQUAL TERMINFO-NOTFOUND)
        message(FATAL_ERROR "no libtinfo or libncurses is found in system")
    else (${TERMINFO} STREQUAL TERMINFO-NOTFOUND)
        target_link_libraries(_${COMPONENT_NAME}_llvm ${TERMINFO})
    endif (${TERMINFO} STREQUAL TERMINFO-NOTFOUND)
endif()
# link the library to its dependencies
# now that we have PatchEnergyJIT stuff, we need the llvm stuff to compile these things
target_link_libraries(_${COMPONENT_NAME}_llvm ${llvm_libs})

# need to link llvm_libs here, too, otherwise module import fails
target_link_libraries(_${COMPONENT_NAME} PRIVATE _${COMPONENT_NAME}_llvm ${HOOMD_LIBRARIES} ${llvm_libs})
#target_link_libraries(_${COMPONENT_NAME} PRIVATE ${HOOMD_LIBRARIES})
#target_link_libraries(_${COMPONENT_NAME} PRIVATE ${HOOMD_LIBRARIES} ${llvm_libs})
# need to link llvm_libs here, too, otherwise module import fails
#target_include_directories(_${COMPONENT_NAME} PRIVATE ${HOOMD_INCLUDE_LIB} ${../${COMPONENT_NAME}})
#target_link_libraries(_${COMPONENT_NAME} PRIVATE ${HOOMD_MD_LIB})
# set installation RPATH
if(APPLE)
set_target_properties(_${COMPONENT_NAME} PROPERTIES INSTALL_RPATH "@loader_path/..;@loader_path")
else()
set_target_properties(_${COMPONENT_NAME} PROPERTIES INSTALL_RPATH "$ORIGIN/..;$ORIGIN")
endif()

# link the libraries to their dependencies
# if we are compiling with MPI support built in, set appropriate
# compiler/linker flags
if (ENABLE_MPI)
   if(MPI_COMPILE_FLAGS)
       set_target_properties(_${COMPONENT_NAME} PROPERTIES COMPILE_FLAGS "${MPI_CXX_COMPILE_FLAGS}")
   endif(MPI_COMPILE_FLAGS)
   if(MPI_LINK_FLAGS)
       set_target_properties(_${COMPONENT_NAME} PROPERTIES LINK_FLAGS "${MPI_CXX_LINK_FLAGS}")
   endif(MPI_LINK_FLAGS)
endif(ENABLE_MPI)

if (ENABLE_DEBUG)
    set_target_properties(_${COMPONENT_NAME} PROPERTIES COMPILE_FLAGS "-DENABLE_DEBUG")
endif(ENABLE_DEBUG)

# tweak the properties of the output to make a functional python module
# I needed these stupid bastards to make things work. I'll comment them out if I really don't need them
#set_target_properties(_${COMPONENT_NAME} PROPERTIES PREFIX "" OUTPUT_NAME "_${COMPONENT_NAME}")
#set_target_properties(_${COMPONENT_NAME} PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)
#set_target_properties(_${COMPONENT_NAME} PROPERTIES INSTALL_RPATH_USE_LINK_PATH TRUE)

# .dylib is not recognized as a python module by python on Mac OS X
if(APPLE)
    set_target_properties(_${COMPONENT_NAME} PROPERTIES SUFFIX ".so")
    #set_target_properties(_${COMPONENT_NAME} PROPERTIES INSTALL_RPATH "@loader_path/..;@loader_path")
    #else()
    #set_target_properties(_${COMPONENT_NAME} PROPERTIES INSTALL_RPATH "$ORIGIN/..;$ORIGIN")
endif(APPLE)

fix_cudart_rpath(_${COMPONENT_NAME})
fix_cudart_rpath(_${COMPONENT_NAME}_llvm)

# install the library
install(TARGETS _${COMPONENT_NAME} _${COMPONENT_NAME}_llvm
        LIBRARY DESTINATION ${PYTHON_MODULE_BASE_DIR}/${COMPONENT_NAME}
        )

################ Python only modules
# copy python modules to the build directory to make it a working python package
MACRO(copy_file file)
    add_custom_command (
        OUTPUT ${file}
        POST_BUILD
        COMMAND    ${CMAKE_COMMAND}
        ARGS       -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file}
        COMMENT    "Copy hoomd/${COMPONENT_NAME}/${file}"
    )
ENDMACRO(copy_file)

set(files   data.py
            __init__.py
            _hpmc_swap.py
            integrate.py
            update.py
            patch.py
    )

install(FILES ${files}
        DESTINATION ${PYTHON_MODULE_BASE_DIR}/${COMPONENT_NAME}
       )

foreach(file ${files})
    copy_file(${file})
endforeach()

add_custom_target(copy_${COMPONENT_NAME} ALL DEPENDS ${files})

#Actual HPMC copy the header files as well. I don't think I really need to copy these dudes
#so I'll just comment them out (for now)
# copy python modules to the build directory to make it a working python package
#MACRO(copy_header file)
#    add_custom_command (
#        OUTPUT ${file}
#        POST_BUILD
#        COMMAND    ${CMAKE_COMMAND}
#        ARGS       -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/../include/hoomd/${COMPONENT_NAME}/${file}
#        COMMENT    "Copy hoomd/include/hoomd/${COMPONENT_NAME}/${file}"
#    )
#ENDMACRO(copy_header)

# install headers in installation target
#install(FILES _${COMPONENT_NAME}_headers
#        DESTINATION ${PYTHON_MODULE_BASE_DIR}/include/hoomd/${COMPONENT_NAME}
#       )

#if (COPY_HEADERS)
# copy headers into build directory
#foreach(file ${_hpmc_headers})
#    copy_header(${file})
#endforeach()

#add_custom_target(copy_hpmc_headers ALL DEPENDS ${_hpmc_headers})
#endif()
