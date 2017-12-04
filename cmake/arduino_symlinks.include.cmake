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

# Setup symlinks that enable correct build for x86 using the
# Arduino build system (inspired by the Hardware-Virtual plugin 
#    https://github.com/cdisselkoen/Kaleidoscope-Hardware-Virtual)
# Thanks to cdisselkoen for the inspiration.
#

# The following scans all Kaleidoscope modules for python wrapper 
# files and generates symbolic links with extension ".cpp". This enables
# the files to be included in the firmware build process.

if(NOT "${KALEIDOSCOPE_HARDWARE_BASE_PATH}" STREQUAL "")
   get_filename_component(arduino_sketchbook_path_default
      "${KALEIDOSCOPE_HARDWARE_BASE_PATH}" PATH)
endif()

set(KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR "${arduino_sketchbook_path_default}" 
   CACHE PATH "The Arduino sketchbook path.")
   
if("${KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR}" EQUAL ""
   OR NOT EXISTS "${KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR}")
   
   message(FATAL_ERROR 
      "Please define an existing KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR")
endif()

set(support_link_name 
   "${KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR}/hardware/keyboardio/x86")
set(support_target "${CMAKE_SOURCE_DIR}/support/x86")
generate_link("${support_target}" "${support_link_name}")

set(libraries_link_name "${CMAKE_SOURCE_DIR}/support/x86/libraries")
set(libraries_target 
   "${KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR}/hardware/keyboardio/avr/libraries")
generate_link("${libraries_target}" "${libraries_link_name}")