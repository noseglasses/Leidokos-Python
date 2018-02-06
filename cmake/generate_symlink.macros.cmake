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
   
      if(CMAKE_HOST_WIN32)
      
         # There is no way to generate symlinks on 
         # Windows without administrative privileges.
         # Copy the file as a workaround.
         #
         if(IS_DIRECTORY "${target_}")
            set(copy_command copy_directory)
         else()
            set(copy_command copy)
         endif()
         
         execute_process(
            COMMAND "${CMAKE_COMMAND}" ${copy_command}
               "${target_}"
               "${link_}"
         )
      else()
   
#       message("Generating symbolic link ${link_} -> ${target_}")
         execute_process(
            COMMAND "${CMAKE_COMMAND}" -E create_symlink "${target_}" "${link_}"
         )
      endif()
   endif()
endfunction()