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

if(CMAKE_HOST_WIN32)

   # See https://stackoverflow.com/questions/4051883/batch-script-how-to-check-for-admin-rights#21295806
   #
   execute_process(
      COMMAND fsutil dirty query $ENV{systemdrive}
      RESULT_VARIABLE result
   )
   
   if(NOT result EQUAL 0)
      message(FATAL_ERROR "On Windows Leidokos-Python configuration phase must be run with administrative privileges. This is necessary to enable the creation of symbolic links which is not possible otherwise.")
   endif()
endif()
      