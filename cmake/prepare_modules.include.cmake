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

include("${CMAKE_SOURCE_DIR}/cmake/generate_symlink.macros.cmake")

# This function is called by Leidokos-CMake as a hook
#
function(after_KALEIDOSCOPE_HARDWARE_BASE_PATH_defined)

   # The build system variable KALEIDOSCOPE_MODULE_REPO_PATHS 
   # can contain a list of repo paths or alternatively a directory
   # that is parent to a number of such repository. File search for 
   # .python-wrapper files is in any case recursive.
   #
   set(KALEIDOSCOPE_MODULE_REPO_PATHS "${KALEIDOSCOPE_HARDWARE_BASE_PATH}" 
      CACHE STRING 
      "A list of paths that are recursively searched for files with \
   extension .python-wrapper .")

   set(repo_paths "${KALEIDOSCOPE_MODULE_REPO_PATHS}")

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
            generate_link("${wrapper_file}" "${cpp_file}")
         endif()
      endforeach()
   endfunction()

   if("${repo_paths}" STREQUAL "")
      message(FATAL_ERROR "No repo information found. Neither via KALEIDOSCOPE_MODULE_REPO_PATHS nor KALEIDOSCOPE_MODULE_REPO_PATHS_FILE.")
   endif()

   message("repo_paths = ${repo_paths}")

   foreach(repo_path ${repo_paths})
      scan_repo("${repo_path}")
   endforeach()
   
endfunction()