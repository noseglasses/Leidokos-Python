#  -*- mode: cmake -*-
# Leidokos-Python -- Wraps Kaleidoscope modules' c++
#    code to be available in Python programs.
# Copyright (C) 2017 noseglasses <shinynoseglasses@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

cmake_minimum_required(VERSION 2.8)

if(CMAKE_HOST_APPLE)
   set(CMAKE_PREFIX_PATH "/usr/local;${CMAKE_PREFIX_PATH}" CACHE STRING "" FORCE)
endif()

# Generate version information. This initializes a CMake variable
#   kaleidoscope_PYTHON_git_version
#   version_cpp_file
#
include("${CMAKE_SOURCE_DIR}/cmake/versioning.include.cmake")

if("${CMAKE_BUILD_TYPE}" STREQUAL "")
   set(CMAKE_BUILD_TYPE "Debug" CACHE STRING "" FORCE)
endif()

# kaleidoscope_cmake_after_configure_platform_hook is called
# by Leidokos-CMake after the target platform (paths) has been configured.
#
macro(kaleidoscope_cmake_after_configure_platform_hook)

   include("${CMAKE_SOURCE_DIR}/cmake/generate_symlink.macros.cmake")

   # Setup symlinks that enable correct build for x86 using the
   # Arduino build system
   #
   include("${CMAKE_SOURCE_DIR}/cmake/arduino_symlinks.include.cmake")
   
   # Find python to determine its link directory
   #
   find_package(PythonLibs 3 REQUIRED)

   if(NOT PYTHONLIBS_FOUND)
      message(SEND_ERROR "Leidokos-Python requires python \
   libraries and headers to compile python wrappers. If you have installed python \
   in a non standard location, please configure the CMake build \
   system accordingly. See the documentation about the FindPythonLibs module \
   at https://cmake.org/cmake/help/v3.0/module/FindPythonLibs.html for \
   additional build system variables that support the python auto \
   detection process.")
      message(SEND_ERROR "Under Ubuntu linux python can be installed as")
      message(SEND_ERROR "sudo apt-get install libboost-python-dev")
      message(FATAL_ERROR "Aborting.")
      
   endif()
   
   # Some additional setup of the Arduino build system is required.
   #
   # Make sure that the arduino build finds boost-python
   #
   find_package(Boost
      REQUIRED
#       COMPONENTS python
   )
   
   # As we need boost-python 3 to build and FindBoost does not allow 
   # to specify a version preference for the Python version that is used,
   # we find the boost_python library explicitly.
   #
   find_library(Boost_PYTHON_3_LIBRARY
    NAMES 
       boost_python-py3 
       boost_python-py31 
       boost_python-py32 
       boost_python-py33 
       boost_python-py34 
       boost_python-py35 
       boost_python-py36 
       boost_python-py37 
       boost_python-py38 
       boost_python-py39

       boost_python3 
       boost_python31 
       boost_python32 
       boost_python33 
       boost_python34 
       boost_python35 
       boost_python36 
       boost_python37 
       boost_python38 
       boost_python39
     HINTS ENV PATH /usr/lib /usr/lib/x86_64-linux-gnu
   )

   if("${Boost_PYTHON_3_LIBRARY}" STREQUAL "Boost_PYTHON_3_LIBRARY-NOTFOUND")
      message("Boost_PYTHON_3_LIBRARY=${Boost_PYTHON_3_LIBRARY}")
      message(SEND_ERROR "Leidokos-Python requires boost-python \
   library (Python 3) and headers to compile python wrappers. If you have installed boost \
   in a non standard location, please configure the CMake build \
   system accordingly.")
      message(SEND_ERROR "Under Ubuntu linux boost python can be installed as")
      message(SEND_ERROR "sudo apt-get install libboost-python-dev")
      message(FATAL_ERROR "Aborting.")
   endif()
   
   # Configures the boards.txt file used by the Arduino build process
   # and add an include directive that points to the boost header location.
   #
   set(LEIDOKOS_PYTHON_BUILD_FLAGS
      "-I${Boost_INCLUDE_DIR} -I${PYTHON_INCLUDE_DIRS} -DKALEIDOSCOPE_HARDWARE_VIRTUAL_NO_LOGGING=1")
      
   # The configure_file command reads a text file, scans it for occurences of
   # CMake variables, as the LEIDOKOS_PYTHON_BUILD_FLAGS
   # variable above, replaces all occurences by the variables value
   # and safes a configured version of the file.
   #
   configure_file(
      "${CMAKE_SOURCE_DIR}/support/x86/boards.txt.in"
      "${CMAKE_SOURCE_DIR}/support/x86/boards.txt"
   )
endmacro()

# Setup the keymap strings file that enables verbose names
# of keys at a given position in the keymap.
#
set(keymap_strings_file "${CMAKE_BINARY_DIR}/keymap_strings.cpp")

message("Extracting keymap to ${keymap_strings_file}")
include("${CMAKE_SOURCE_DIR}/cmake/extract_keymap.macros.cmake")

get_filename_component(firmware_sketch_real 
   "${KALEIDOSCOPE_FIRMWARE_SKETCH}" REALPATH)
   
message("sketch: ${firmware_sketch_real}")
   
extract_keymap(
   "${firmware_sketch_real}"
   "${keymap_strings_file}"
   keymap_extraction_success
)

# This configuration process can be passed a list of paths that 
# point to Kaleidoscope components (git repos).
#
# All defined repos are scanned for files that end with .python-wrapper.
# For every such file, a symbolic link with the extension .cpp is created
# in the same directory as the orginal file.
# This enables the wrapper files only to be visible during firmware 
# builds that explicitly require python wrapping. All files with extension 
# .python-wrapper are otherwise invisible to the Kaleidoscope Arduino
# build system.
#
# Files with extension .python-wrapper are treated as c++ implementation
# files and expected to rely on boost python (www.boost.org) for
# automatic wrapping of c++ classes, functions, objects and POD instances.
# 
# The configuration checks for boost python to be available and
# configures the Arduino build system accodingly.

# As we have to link some external libraries to the virtual
# firmware, we cannot build it using kaleidoscope-builder.
# Thus, we rely on Leidokos-CMake to build.
#
set(LEIDOKOS_CMAKE_SOURCE_DIR 
   "${CMAKE_SOURCE_DIR}/3rd_party/Leidokos-CMake"
   CACHE INTERNAL "")
   
set(KALEIDOSCOPE_ARCHITECTURE_ID "x86" CACHE STRING 
   "The architecture id of the board to build a firmware for.")
set(KALEIDOSCOPE_BOARD "virtual" CACHE STRING
   "The type of board hardware.")
set(KALEIDOSCOPE_HOST_BUILD TRUE CACHE INTERNAL "")

# Make sure the Kaleidoscope-Hardware-Virtual submodule is found
#
include_directories(
   "${CMAKE_SOURCE_DIR}/3rd_party/Kaleidoscope-Hardware-Virtual"
   "${CMAKE_SOURCE_DIR}/3rd_party/Kaleidoscope-Hardware-Virtual/src"
   "${CMAKE_SOURCE_DIR}/3rd_party/Kaleidoscope-Hardware-Virtual/src/Kaleidoscope")

# kaleidoscope_set_binary_basename_hook is called by Kaleidoscope_CMake 
# during intialization.
# The reason for its existence is that we cannot define the firmware 
# executable basename here directly as we require 
# variable CMAKE_SHARED_LIBRARY_SUFFIX
# which is only set later on during initialization when project(...) 
# is called.
#
macro(kaleidoscope_set_binary_basename_hook 
   basename_var_
)
   # Important: On MacOS python modules are bundles (extension .so not .dylib)
   #
   if(CMAKE_HOST_APPLE)
      set(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
   endif()
   
   set(${basename_var_} "kaleidoscope${CMAKE_SHARED_LIBRARY_SUFFIX}")
endmacro()

# Adding a dummy header that forces the Kaleidoscope-Hardware-Virtual
# module to be included in the firmware build.
#
set(KALEIDOSCOPE_ADDITIONAL_HEADERS 
   "${CMAKE_SOURCE_DIR}/src/Leidokos-Python.h" CACHE INTERNAL "")
   
file(GLOB_RECURSE add_src 
   "${CMAKE_SOURCE_DIR}/3rd_party/Kaleidoscope-Hardware-Virtual/src/*.cpp")

set(KALEIDOSCOPE_ADDITIONAL_SOURCES 
   "${KALEIDOSCOPE_ADDITIONAL_SOURCES};${add_src};${keymap_strings_file}" CACHE INTERNAL "")
   
# Prepare any Kaleidoscope modules by calling their initialization scripts.
#
include("${CMAKE_SOURCE_DIR}/cmake/prepare_modules.include.cmake")
   
# Even though we do no use Arduino for virtual builds, the variable 
# ARDUINO_SDK_VERSION to be set. Else arduino-cmake will fail.
#
set(ARDUINO_SDK_VERSION "1.8.5")
set(ARDUINO_SDK_VERSION_MAJOR 1)
set(ARDUINO_SDK_VERSION_MINOR 8)
set(ARDUINO_SDK_VERSION_PATCH 5)

# Disable device upload which is not required for virtual builds
#
set(LEIDOKOS_CMAKE_NO_DEVICE_UPLOAD TRUE)

# Include the Leidokos-CMake build system
#
include("${CMAKE_SOURCE_DIR}/3rd_party/Leidokos-CMake/CMakeLists.txt")

# By convention, CMake requires a project(...) directive in the
# toplevel CMakeLists.txt file to be present. Any following
# project directives seem to be ignored. The following is only a dummy.
# The actual project definition is done by the included Leidokos-CMake
# build system.
#
project(Kaleidoscope)

# Set policy to prevent file globbing through symlinks. This must be
# explicitly set to NEW to silencd warnings of recent CMake versions.
#
cmake_policy(SET CMP0009 NEW)

# Let the boost python and python libraries be linked with the 
# firmware.
#
target_link_libraries("${kaleidoscope_firmware_target}"
   PUBLIC
   "${Boost_PYTHON_3_LIBRARY}"
   "${PYTHON_LIBRARY}"
)

# Setup Python API documentation
#
include("${CMAKE_SOURCE_DIR}/cmake/api_doc.include.cmake")

# Add some additional header search directories. This is just for 
# IDEs to find the appropriate files (language parsers).
#
include_directories(
   "${CMAKE_SOURCE_DIR}/src"
   "${CMAKE_SOURCE_DIR}/../Kaleidoscope/src"
)
