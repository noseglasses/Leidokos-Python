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

cmake_minimum_required(VERSION 2.8)

# Set policy to prevent file globbing through symlinks
#
cmake_policy(SET CMP0009 NEW)

# The build system variable KALEIDOSCOPE_MODULE_REPO_PATHS 
# can contain a list of repo paths or alternatively a directory
# that is parent to a number of such repository. File search for 
# .python-wrapper files is in any case recursive.
#
set(KALEIDOSCOPE_MODULE_REPO_PATHS "" CACHE STRING "A list of paths that are recursively searched for files with extension .python-wrapper")

set(repo_paths "${KALEIDOSCOPE_MODULE_REPO_PATHS}")

# A list of repo paths can also be defined in a file whose filename
# is provided through the variable KALEIDOSCOPE_MODULE_REPO_PATHS_FILE
#
set(KALEIDOSCOPE_MODULE_REPO_PATHS_FILE "" CACHE FILEPATH "A text file that contains a list of paths (one per line) that are recursively searched for files with extension .python-wrapper")

if(EXISTS "${KALEIDOSCOPE_MODULE_REPO_PATHS_FILE}")

   file(READ "${file}" contents)

   # Convert file contents into a CMake list (where each element in the list
   # is one line of the file)
   #
   string(REGEX REPLACE ";" "\\\\;" contents "${contents}")
   string(REGEX REPLACE "\n" ";" contents "${contents}")
   
   list(APPEND repo_paths "${contents}")
endif()

function(generate_link 
   target_ 
   link_
)
   if(NOT EXISTS "${link_}")
   
      message("Generating symbolic link ${link_} -> ${target_}")
      execute_process(
         COMMAND "${CMAKE_COMMAND}" -E create_symlink "${target_}" "${link_}"
      )
   endif()
endfunction()

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
   message(SEND_ERROR "Kaleidoscope-Python-Wrapper requires boost-python library and headers to compile python wrappers. If you have installed boost in a non standard location, please configure the CMake build system accordingly. See the documentation about the FindBoost module at https://cmake.org/cmake/help/v3.0/module/FindBoost.html for additional build system variables that support the boost auto detection process.")
   message(SEND_ERROR "Under Ubuntu linux boost python can be installed as")
   message(SEND_ERROR "sudo apt-get install libboost-python-dev")
   message(FATAL_ERROR "Aborting.")
endif()
   
# Find python to determine its link directory
#
find_package(PythonLibs REQUIRED)

if(NOT PYTHONLIBS_FOUND)
   message(SEND_ERROR "Kaleidoscope-Python-Wrapper requires python libraries and headers to compile python wrappers. If you have installed python in a non standard location, please configure the CMake build system accordingly. See the documentation about the FindPythonLibs module at https://cmake.org/cmake/help/v3.0/module/FindPythonLibs.html for additional build system variables that support the python auto detection process.")
   message(SEND_ERROR "Under Ubuntu linux python can be installed as")
   message(SEND_ERROR "sudo apt-get install libboost-python-dev")
   message(FATAL_ERROR "Aborting.")
   
endif()
   
# Configure the boards.txt file used by the Arduino build process
# and add an include directive that points to the boost header location.
#
set(KALEIDOSCOPE_PYTHON_WRAPPER_BUILD_FLAGS
   "\"-I${Boost_INCLUDE_DIR}\" \"-I${PYTHON_INCLUDE_DIRS}\"")
   
# The configure_file command reads a text file, scans it for occurences of
# CMake variables, as the KALEIDOSCOPE_PYTHON_WRAPPER_BUILD_FLAGS
# variable above, replaces all occurences by the variables value
# and safes a configured version of the file.
#
configure_file(
   "${CMAKE_SOURCE_DIR}/support/x86/boards.txt.in"
   "${CMAKE_BINARY_DIR}/support/x86/boards.txt"
)

# Setup symlinks that enable correct build for x86 using the
# Arduino build system (inspired by the Hardware-Virtual plugin 
#    https://github.com/cdisselkoen/Kaleidoscope-Hardware-Virtual)
# Thanks to cdisselkoen for the inspiration.
#
set(KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR "" CACHE PATH "The Arduino sketchbook path")
if("${KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR}" EQUAL ""
   OR NOT EXISTS "${KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR}")
   
   message(FATAL_ERROR "Please define an existing KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR")
endif()

set(support_link_name "${KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR}/hardware/keyboardio/x86")
set(support_target "${CMAKE_SOURCE_DIR}/support/x86")
generate_link("${support_target}" "${support_link_name}")

set(libraries_link_name "${${CMAKE_SOURCE_DIR}/support/x86/libraries}")
set(libraries_target "${KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR}/hardware/keyboardio/avr/libraries")