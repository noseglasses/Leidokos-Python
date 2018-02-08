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

function(generate_link 
   target_ 
   link_
)
   if(NOT EXISTS "${link_}")

      message("Generating link ${link_} -> ${target_}")
      
      if(CMAKE_HOST_WIN32)
      
         if(IS_DIRECTORY "${target_}")
            set(flag "/J")
#             set(flag "/D")
         else()
            set(flag "/H")
#             set(flag)
         endif()
         
         get_filename_component(link_location "${link_}" DIRECTORY)
         
         if(NOT EXISTS "${link_location}")
            file(MAKE_DIRECTORY "${link_location}")
         endif()
         
         if(NOT EXISTS "${target_}")
            message(FATAL_ERROR "Unable to create link ${link_}, the target ${target_} does not exist")
         endif()
         
         if(NOT IS_DIRECTORY "${link_location}") 
            message(FATAL_ERROR "Unable to create link ${link_}, the location ${link_location} does not exist")
         endif()
         
         file(TO_NATIVE_PATH "${link_}" link_native)
         string(REPLACE "/" "\\" link_native "${link_native}")
         file(TO_NATIVE_PATH "${target_}" target_native)
         string(REPLACE "/" "\\" target_native "${target_native}")
         
         execute_process(
            COMMAND cmd /c mklink ${flag} "${link_native}" "${target_native}" 
            RESULT_VARIABLE result
            OUTPUT_VARIABLE output
            ERROR_VARIABLE error
         )
         message("Link:")
         execute_process(
            COMMAND cmd /c dir "${link_native}"
         )
         message("Target:")
         execute_process(
            COMMAND cmd /c dir "${target_native}"
         )
         if(NOT result EQUAL 0)
            message("Failed generating link ${link_native} -> ${target_native}")
            message("result = ${result}")
            message("output = ${output}")
            message("error = ${error}")
            message(FATAL_ERROR "Bailing out.")
         endif()
      else()
   
         execute_process(
            COMMAND "${CMAKE_COMMAND}" -E create_symlink "${target_}" "${link_}"
            RESULT_VARIABLE result
            OUTPUT_VARIABLE output
            ERROR_VARIABLE error
         )
      
         if(NOT result EQUAL 0)
            message("Failed generating link ${link_} -> ${target_}")
            message("result = ${result}")
            message("output = ${output}")
            message("error = ${error}")
            message(FATAL_ERROR "Bailing out.")
         endif()
      endif()
   endif()
endfunction()