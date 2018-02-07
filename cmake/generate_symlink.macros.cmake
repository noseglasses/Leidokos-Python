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
   
#       if(CMAKE_HOST_WIN32)
#       
#          # There is no way to generate symlinks on 
#          # Windows without administrative privileges.
#          # Copy the file as a workaround.
#          #  
#          message("Copying ${target_} to ${link_}")
#          get_filename_component(target_dir "${link_}" DIRECTORY)
#          file(MAKE_DIRECTORY "${target_dir}")
#          
#          execute_process(
#             COMMAND "${CMAKE_COMMAND}" copy
#                "${target_}"
#                "${link_}"
#          )
#       else()
      message("Generating link ${link_} -> ${target_}")
      
      if(CMAKE_HOST_WIN32)
      
         if(IS_DIRECTORY "${target_}")
            set(flag "/J")
         else()
            set(flag "/H")
         endif()
         
         execute_process(
            COMMAND mklink.exe ${flag} "${link_}" "${target_}" 
            RESULT_VARIABLE result
            OUTPUT_VARIABLE output
            ERROR_VARIABLE error
         )
      else()
   
         execute_process(
            COMMAND "${CMAKE_COMMAND}" -E create_symlink "${target_}" "${link_}"
            RESULT_VARIABLE result
            OUTPUT_VARIABLE output
            ERROR_VARIABLE error
         )
      endif()
      
      if(NOT result EQUAL 0)
         message("Failed generating link ${link_} -> ${target_}")
         message("result = ${result}")
         message("output = ${output}")
         message("error = ${error}")
         message(FATAL_ERROR "Bailing out.")
      endif()
   endif()
endfunction()