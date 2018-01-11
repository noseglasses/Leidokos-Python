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

function(extract_keymap
   sketch_file_abspath_
   keymap_file_abspath_
   keymap_file_created_var_
)
   file(READ "${sketch_file_abspath_}" sketch_file_content)
   
#    message("${sketch_file_content}")

   string(REGEX MATCH 
    "const[\t ]+Key[\t ]+keymaps[\t ]*[^{]+(([^;]|[\n\r])*)"
#     "const[\t ]+Key[\t ]+keymaps[\t ]*"
    tmp "${sketch_file_content}") 
    
#    message("CMAKE_MATCH_0 = ${CMAKE_MATCH_0}")
#    message("CMAKE_MATCH_1 = ${CMAKE_MATCH_1}")
    
   set(keymap_def "${CMAKE_MATCH_1}")
   
   if("${keymap_def}" STREQUAL "")
      message(WARNING "Keymap extraction failed")
      set(${keymap_file_created_var_} FALSE PARENT_SCOPE)
      return()
   endif()
   
   string(REGEX REPLACE "\\[[ \t]*[A-Za-z0-9_]+[ \t]*\\][ \t]*=[ \t]*KEYMAP_STACKED" "__KEYMAP_STACKED" 
      keymap_def "${keymap_def}") 
      
   string(REPLACE "\\[[ \t]*[A-Za-z0-9_]+[ \t]*\\][ \t]*=[ \t]*KEYMAP" "__KEYMAP" 
      keymap_def "${keymap_def}") 
   
   file(WRITE "${keymap_file_abspath_}"
"
#include KALEIDOSCOPE_HARDWARE_H

#include \"KVP_Preprocessor_Macro_Map.h\"

#include <cstdint>

#define __QUOTE(S) #S
#define QUOTE(S) __QUOTE(S)

#define ___KEYMAP(...) KEYMAP(__VA_ARGS__)
#define __KEYMAP(...) ___KEYMAP(MAP_LIST(QUOTE, __VA_ARGS__))

#define ___KEYMAP_STACKED(...) KEYMAP_STACKED(__VA_ARGS__)
#define __KEYMAP_STACKED(...) ___KEYMAP_STACKED(MAP_LIST(QUOTE, __VA_ARGS__))

namespace kaleidoscope {

static const char *keymap_strings__[][ROWS][COLS] = ${keymap_def};

const char *key_description(uint8_t layer, uint8_t row, uint8_t col) {
   return keymap_strings__[layer][row][col];
}

}; // namespace kaleidoscope
"
)
endfunction()