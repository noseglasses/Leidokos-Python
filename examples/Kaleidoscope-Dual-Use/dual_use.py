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

def bitRead(value, bit):
   return ((value) >> (bit)) & 0x01

def bitSet(value, bit):
   res = value | (1 << (bit))
   return value | (1 << (bit))

def bitClear(value, bit):
   return value & ~(1 << (bit))

def bitWrite(value, bit, bitvalue):
   if bitvalue == 1:
      return bitSet(value, bit)
   return bitClear(value, bit)

class DualUse(object):
   
   def __init__(self):
      self.key_action_needed_map_ = 0
      self.pressed_map_ = 0
      self.end_time_ = 0
      self.time_out = 1000
      
   def specialAction(self, spec_index):
      new_key = Key()

      new_key.setFlags = KEY_FLAGS()
   
      if spec_index < 8:
         new_key.setKeyCode(keyLeftControl().getKeyCode() + spec_index)
      else:
         target = spec_index - 8

         Layer.on(target)

         new_key.setFeyCode(0)
         
      return new_key

   def pressAllSpecials(self, row, col):
      for spec_index in range(0, 32):
         if not bitRead(self.pressed_map_, spec_index):
            continue

         new_key = self.specialAction(spec_index)
    
         if new_key.getRaw() != keyNoKey().getRaw():
            handleKeyswitchEvent(new_key, row, col, IS_PRESSED() | INJECTED())

   def inject(self, key, key_state):
      # Note: 255 sets the unknown keyswitch location
      #
      eventHandlerHook(key, 255, 255, key_state)

   def eventHandlerHook(self, mapped_key, row, col, key_state):
      
      if key_state & INJECTED():
         return mapped_key

      # If nothing happened, bail out fast.
      if not keyIsPressed(key_state) and not keyWasPressed(key_state):
         if (mapped_key.getRaw() < ranges.DU_FIRST()) or (mapped_key.getRaw() > ranges.DU_LAST()):
            return mapped_key
         return keyNoKey()
      
      if (mapped_key.getRaw() >= ranges.DU_FIRST()) and (mapped_key.getRaw() <= ranges.DU_LAST()):
          
         spec_index = (mapped_key.getRaw() - ranges.DU_FIRST()) >> 8
         new_key = keyNoKey()

         if keyToggledOn(key_state):
            self.pressed_map_ = bitWrite(self.pressed_map_, spec_index, 1)
            self.key_action_needed_map_ = bitWrite(self.key_action_needed_map_, spec_index, 1)
            self.end_time_ = millis() + self.time_out
            
         elif keyIsPressed(key_state):
            if millis() >= self.end_time_:
               new_key = self.specialAction(spec_index)
               self.key_action_needed_map_ = bitWrite(self.key_action_needed_map_, spec_index, 0)
            
         elif keyToggledOff(key_state):
            if (millis() < self.end_time_) and bitRead(self.key_action_needed_map_, spec_index):
               m = mapped_key.getRaw() - ranges.DU_FIRST() - (spec_index << 8)
               if (spec_index >= 8):
                  m = m - 1

               new_key = Key(m, KEY_FLAGS())

               handleKeyswitchEvent(new_key, row, col, IS_PRESSED() | INJECTED())
               hid.sendKeyboardReport()
            else:
               if (spec_index >= 8):
                  target = spec_index - 8

                  Layer.off(target)

            self.pressed_map_ = bitWrite(self.pressed_map_, spec_index, 0)
            self.key_action_needed_map_ = bitWrite(self.key_action_needed_map_, spec_index, 0)

         return new_key

      if (self.pressed_map_ == 0):
         return mapped_key

      self.pressAllSpecials(row, col)
      self.key_action_needed_map_ = 0

      if (self.pressed_map_ > (1 << 7)):
         mapped_key = Layer.lookup(row, col)

      return mapped_key

class DualUseTest(Test):

   def checkDualUsePrimaryFunction(self):
      
      self.header("Checking DualUse primary function")
         
      # Press the Dual Use key alone. This is supposed to result in the number '1'
      # being emitted.
      #
      self.keyDown(0, 1)

      # The dual use key does only emit its primary key once it is released
      #
      self.scanCycle([CycleHasNReports(0)])

      # Make sure that there are no other report once the keys remain held.
      #
      self.scanCycles(2, cycleAssertionList = [CycleHasNReports(0)])

      # Release the dual use key
      #
      self.keyUp(0, 1)

      self.queueGroupedReportAssertions([ 
            ReportKeysActive([key1()], exclusively = True),
            ReportAllModifiersInactive()
         ])
      self.scanCycle([CycleHasNReports(1)])

      self.queueGroupedReportAssertions([ 
            ReportEmpty()
         ])
      self.scanCycle([CycleHasNReports(1)])

      # Make sure that there are no other report once the keys have been released.
      #
      self.scanCycles(2, cycleAssertionList = [CycleHasNReports(0)])
      
   def run(self):

      self.checkDualUsePrimaryFunction()
      self.checkDualUseSecondaryFunction()
      
   def checkDualUseSecondaryFunction(self):
      
      self.header("Checking DualUse secondary function")

      # All reports are supposed to be dumped, i.e. we want to get the
      # keys and modifiers that are acutally active listed.
      #
      self.addPermanentReportAssertions([DumpReport()])

      # Press the Dual Use key and another one
      #
      self.keyDown(0, 1)
      self.keyDown(0, 2)

      # Make sure that the Dual Use key causes left control to be active
      #
      self.queueGroupedReportAssertions([ 
            ReportKeyActive(key2()),
            ReportModifierActive(keyLeftControl())
         ])

      self.scanCycle([CycleHasNReports(1)])

      # Make sure that there are no other report once the keys remain held.
      #
      self.scanCycles(2, cycleAssertionList = [CycleHasNReports(0)])

      # Release the keys again.
      #
      self.keyUp(0, 2)
      self.keyUp(0, 1)

      # Ensure that the next report shows all keys and modifiers to be cleared.
      #
      self.queueGroupedReportAssertions([ 
            ReportEmpty()
         ])
      self.scanCycle([CycleHasNReports(1)])

      # Make sure that there are no other report once the keys have been released.
      #
      self.scanCycles(2, cycleAssertionList = [CycleHasNReports(0)])

def main():
    
   test = DualUseTest()
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
                   
if __name__ == "__main__":
    main()
