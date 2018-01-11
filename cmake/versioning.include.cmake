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

find_package(Git)

if(NOT DEFINED GIT_EXECUTABLE OR ("${GIT_EXECUTABLE}" STREQUAL "GIT_EXECUTABLE-NOTFOUND"))
   message(FATAL_ERROR "Unable to find git. Please secify the location of th egit executable through the variable GIT_EXECUTABLE")
endif()

execute_process(
   COMMAND ${GIT_EXECUTABLE} describe --exact-match HEAD
   OUTPUT_VARIABLE kaleidoscope_PYTHON_git_version
   ERROR_VARIABLE error_out
   RESULT_VARIABLE result
   OUTPUT_STRIP_TRAILING_WHITESPACE
   ERROR_STRIP_TRAILING_WHITESPACE
   WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
)

if((NOT "${result}" STREQUAL "0") OR (NOT "${error_out}" STREQUAL ""))

   # If the search string was found, this means that this is not a tagged ref, so we define the ref
   # using git describe
   #
   execute_process(
      COMMAND ${GIT_EXECUTABLE} describe
      OUTPUT_VARIABLE kaleidoscope_PYTHON_git_version
      ERROR_VARIABLE error_out
      RESULT_VARIABLE result
      OUTPUT_STRIP_TRAILING_WHITESPACE
      WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
   )
   
   if((NOT "${result}" STREQUAL "0") OR (NOT "${error_out}" STREQUAL ""))
      execute_process(
         COMMAND ${GIT_EXECUTABLE} rev-parse --verify HEAD
         OUTPUT_VARIABLE kaleidoscope_PYTHON_git_version
         ERROR_VARIABLE error_out
         RESULT_VARIABLE result
         OUTPUT_STRIP_TRAILING_WHITESPACE
         WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
      )
      
      if((NOT "${result}" STREQUAL "0") OR (NOT "${error_out}" STREQUAL ""))
         message("error_out: ${error_out}")
         message("kaleidoscope_PYTHON_git_version: ${kaleidoscope_PYTHON_git_version}")
         message(FATAL_ERROR "Unable to determine git version information")
      endif()
   endif()
endif()

message("################################################################################")
message("Configuring Leidokos-Python ${kaleidoscope_PYTHON_git_version}")
message("################################################################################")

# Generate a c++ source code file that allows to query version
# information
#
set(version_cpp_file_in "${CMAKE_SOURCE_DIR}/src/KPV_Versioning.cpp.in")
set(version_cpp_file "${CMAKE_BINARY_DIR}/KPV_Versioning.cpp")

configure_file("${version_cpp_file_in}" "${version_cpp_file}")

list(APPEND KALEIDOSCOPE_ADDITIONAL_SOURCES "${version_cpp_file}")
