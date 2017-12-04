#  -*- mode: cmake -*-
# Kaleidoscope-Python-Wrapper -- Wraps Kaleidoscope modules' c++
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

# Generate version information. This initializes a CMake variable
#   kaleidoscope_python_wrapper_git_version
#   version_cpp_file
#
include("${CMAKE_SOURCE_DIR}/cmake/versioning.include.cmake")

# kaleidoscope_cmake_after_configure_platform_hook is called
# by Kaleidoscope-CMake after the target platform (paths) has been configured.
#
macro(kaleidoscope_cmake_after_configure_platform_hook)

   message("Generating links")

   include("${CMAKE_SOURCE_DIR}/cmake/generate_symlink.macros.cmake")

   # Setup symlinks that enable correct build for x86 using the
   # Arduino build system
   #
   include("${CMAKE_SOURCE_DIR}/cmake/arduino_symlinks.include.cmake")
endmacro()

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
# Thus, we rely on Kaleidoscope-CMake to build.
#
set(KALEIDOSCOPE_CMAKE_SOURCE_DIR 
   "${CMAKE_SOURCE_DIR}/3rd_party/Kaleidoscope-CMake"
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
   "${CMAKE_SOURCE_DIR}/3rd_party/Kaleidoscope-Hardware-Virtual/src")

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
   set(${basename_var_} "_kaleidoscope${CMAKE_SHARED_LIBRARY_SUFFIX}")
endmacro()

# Adding a dummy header that forces the Kaleidoscope-Hardware-Virtual
# module to be included in the firmware build.
#
set(KALEIDOSCOPE_ADDITIONAL_HEADERS 
   "${CMAKE_SOURCE_DIR}/src/Kaleidoscope-Python-Wrapper.h" CACHE INTERNAL "")

# Include the Kaleidoscope-CMake build system
#
include("${CMAKE_SOURCE_DIR}/3rd_party/Kaleidoscope-CMake/CMakeLists.txt")

# By convention, CMake requires a project(...) directive in the
# toplevel CMakeLists.txt file to be present. Any following
# project directives seem to be ignored. The following is only a dummy.
# The actual project definition is done by the included Kaleidoscope-CMake
# build system.
#
project(Kaleidoscope)

# Set policy to prevent file globbing through symlinks. This must be
# explicitly set to NEW to silencd warnings of recent CMake versions.
#
cmake_policy(SET CMP0009 NEW)

message("KALEIDOSCOPE_HARDWARE_BASE_PATH=${KALEIDOSCOPE_HARDWARE_BASE_PATH}")

# The build system variable KALEIDOSCOPE_MODULE_REPO_PATHS 
# can contain a list of repo paths or alternatively a directory
# that is parent to a number of such repository. File search for 
# .python-wrapper files is in any case recursive.
#
set(KALEIDOSCOPE_MODULE_REPO_PATHS "${KALEIDOSCOPE_HARDWARE_BASE_PATH}" 
   CACHE STRING 
   "A list of paths that are recursively searched for files with \
extension .python-wrapper .")

message("KALEIDOSCOPE_MODULE_REPO_PATHS=${KALEIDOSCOPE_MODULE_REPO_PATHS}")

set(repo_paths "${KALEIDOSCOPE_MODULE_REPO_PATHS}")
message("repo_paths=${repo_paths}")

# A list of repo paths can also be defined in a file whose filename
# is provided through the variable KALEIDOSCOPE_MODULE_REPO_PATHS_FILE
#
set(KALEIDOSCOPE_MODULE_REPO_PATHS_FILE ""
   CACHE FILEPATH 
   "A text file that contains a list of paths (one per line) that \
are recursively searched for files with extension .python-wrapper .")

if(EXISTS "${KALEIDOSCOPE_MODULE_REPO_PATHS_FILE}")

   file(READ "${file}" contents)

   # Convert file contents into a CMake list (where each element in the list
   # is one line of the file)
   #
   string(REGEX REPLACE ";" "\\\\;" contents "${contents}")
   string(REGEX REPLACE "\n" ";" contents "${contents}")
   
   list(APPEND repo_paths "${contents}")
endif()

function(scan_repo 
   repo_path_
)
   # Find all wrapper files
   #
   file(GLOB_RECURSE wrapper_files "${repo_path_}/*.python-wrapper")
   
   # Generate symbolic links, named# .python-wrapper.cpp for
   # every wrapper file found
   #
   foreach(wrapper_file ${wrapper_files})
   
      set(cpp_file "${wrapper_file}.cpp")
      
      if(NOT EXISTS "${cpp_file}")
      
         message("Generating symbolic link ${cpp_file} -> ${wrapper_file}")
         generate_link("${wrapper_file}" "${cpp_file}")
      endif()
   endforeach()
endfunction()

if("${repo_paths}" STREQUAL "")
   message(FATAL_ERROR "No repo information found. Neither via KALEIDOSCOPE_MODULE_REPO_PATHS nor KALEIDOSCOPE_MODULE_REPO_PATHS_FILE.")
endif()

foreach(repo_path ${repo_paths})
   scan_repo("${repo_path}")
endforeach()

# Some additional setup of the Arduino build system is required.
#
# Make sure that the arduino build finds boost-python
#
find_package(Boost
   REQUIRED
   COMPONENTS python
)

if(NOT Boost_FOUND)
   message(SEND_ERROR "Kaleidoscope-Python-Wrapper requires boost-python \
library and headers to compile python wrappers. If you have installed boost \
in a non standard location, please configure the CMake build \
system accordingly. See the documentation about the FindBoost module \
at https://cmake.org/cmake/help/v3.0/module/FindBoost.html for additional \
build system variables that support the boost auto detection process.")
   message(SEND_ERROR "Under Ubuntu linux boost python can be installed as")
   message(SEND_ERROR "sudo apt-get install libboost-python-dev")
   message(FATAL_ERROR "Aborting.")
endif()
   
# Find python to determine its link directory
#
find_package(PythonLibs REQUIRED)

if(NOT PYTHONLIBS_FOUND)
   message(SEND_ERROR "Kaleidoscope-Python-Wrapper requires python \
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
   
# Configures the boards.txt file used by the Arduino build process
# and add an include directive that points to the boost header location.
#
set(KALEIDOSCOPE_PYTHON_WRAPPER_BUILD_FLAGS
   "-I${Boost_INCLUDE_DIR} -I${PYTHON_INCLUDE_DIRS}")
   
# The configure_file command reads a text file, scans it for occurences of
# CMake variables, as the KALEIDOSCOPE_PYTHON_WRAPPER_BUILD_FLAGS
# variable above, replaces all occurences by the variables value
# and safes a configured version of the file.
#
configure_file(
   "${CMAKE_SOURCE_DIR}/support/x86/boards.txt.in"
   "${CMAKE_BINARY_DIR}/support/x86/boards.txt"
)

# Let the boost python and python libraries be linked with the 
# firmware.
#
target_link_libraries("${kaleidoscope_firmware_target}"
   PUBLIC
   "${Boost_LIBRARIES}"
   "${PYTHON_LIBRARY}"
)

# Setup Python API documentation
#
include("${CMAKE_SOURCE_DIR}/cmake/api_doc.include.cmake")