#!/usr/bin/python

# -*- mode: c++ -*-
# Kaleidoscope-Python -- Wraps Kaleidoscope modules' c++
#    code to be available in Python programs.
# Copyright (C) 2017 noseglasses <shinynoseglasses@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This is a python based implementation of the Kaleidoscope-Dual-Use plugin
#
# It demonstrates how plugins can be prototyped with Kaleidoscope-Python
# before finally implementing them as C++ code.

import kaleidoscope
from kaleidoscope import *

import argparse
import sys

keynames = {
  "1": [0, 1],
  "2": [0, 2],
  "3": [0, 3],
  "4": [0, 4],
  "5": [0, 5],
  "led": [0, 6],
  "any": [0, 9],
  "6": [0, 10],
  "7": [0, 11],
  "8": [0, 12],
  "9": [0, 13],
  "0": [0, 14],
  "num": [0, 15],
  "`": [1, 0],
  "q": [1, 1],
  "w": [1, 2],
  "e": [1, 3],
  "r": [1, 4],
  "t": [1, 5],
  "tab": [1, 6],
  "enter": [1, 9],
  "y": [1, 10],
  "u": [1, 11],
  "i": [1, 12],
  "o": [1, 13],
  "p": [1, 14],
  "=": [1, 15],
  "pgup": [2, 0],
  "a": [2, 1],
  "s": [2, 2],
  "d": [2, 3],
  "f": [2, 4],
  "g": [2, 5],
  "h": [2, 10],
  "j": [2, 11],
  "k": [2, 12],
  "l": [2, 13],
  ";": [2, 14],
  "'": [2, 15],
  "pgdn": [3, 0],
  "z": [3, 1],
  "x": [3, 2],
  "c": [3, 3],
  "v": [3, 4],
  "b": [3, 5],
  "esc": [2, 6],
  "fly": [2, 9],
  "n": [3, 10],
  "m": [3, 11],
  ",": [3, 12],
  ".": [3, 13],
  "/": [3, 14],
  "-": [3, 15],
  "lctrl": [0, 7],
  "bksp": [1, 7],
  "cmd": [2, 7],
  "lshift": [3, 7],
  "rshift": [3, 8],
  "alt": [2, 8],
  "space": [1, 8],
  "rctrl": [0, 8],
  "lfn": [3, 6],
  "rfn": [3, 9]
}

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quam est, tincidunt eu nunc gravida, ultricies varius ipsum. Nulla consectetur facilisis mauris vitae tincidunt. Vivamus pulvinar tristique tortor maximus vestibulum. Quisque eget ligula nisi. Vestibulum ac risus varius, sollicitudin eros ac, ornare nibh. Suspendisse in tortor mollis, tempor nulla et, volutpat mauris. Nullam eget suscipit risus. Cras fringilla molestie mi eget viverra. Vivamus accumsan ultricies volutpat. Ut sollicitudin fermentum eros, sed sollicitudin arcu posuere quis. Maecenas pellentesque risus libero. Donec elementum dictum nulla eget tristique. Vestibulum mattis quis metus sit amet ornare. Aliquam blandit, eros vel consequat blandit, leo dui tempor ante, quis vehicula urna metus sit amet libero. Donec venenatis risus nunc, faucibus pellentesque nunc laoreet vitae."

class HeatMapTest(Test):
      
   def run(self):
      
      self.header("Checking HeatMap plugin")
      
      row = 0
      col = 0
      for char in text:
         
         lower_char = char.lower()
         
         if not lower_char in keynames.keys():
            continue
            
         if self.isKeyPressed(row, col):
            self.keyUp(row, col)
            
         [row, col] = keynames[lower_char]
         
         self.keyDown(row, col)
         
         self.scanCycle()

def main():
    
   test = HeatMapTest()
   test.debug = True
   
   parser = argparse.ArgumentParser( 
      description = 
       "This tests the functionality of the Kaleidoscope-DualUse plugin.")

   parser.add_argument('-p', '--use_python_implementation', 
      action='store_true',
      default=False,
      help     = 'Toggles use of the python implementation of DualUse'
   )
                   
   args = parser.parse_args()
   
   if args.use_python_implementation:
      
      test.log("Using Python implementation of DualUse")
      
      dualUse = DualUse()

      Kaleidoscope_.useEventHandlerHook(dualUse)
   
   else:
      test.log("Using C++ implementation of DualUse")
      
   test.run()
   
   test.graphicalMap()
   
   return test
                   
if __name__ == "__main__":
   global test
   test = main()
