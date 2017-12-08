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

import sys

def bitRead(value, bit):
   return ((value) >> (bit)) & 0x01

def bitSet(value, bit):
   return value | (1 << (bit))

def bitClear(value, bit):
   return value & ~(1 << (bit))

def bitWrite(value, bit, bitvalue):
   if bitvalue == 0:
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
            handleKeyswitchEvent(new_key, row, col, IS_PRESSED() | IS_INJECTED())

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
            bitWrite(self.pressed_map_, spec_index, 1)
            bitWrite(self.key_action_needed_map_, spec_index, 1)
            end_time_ = millis() + self.time_out
         elif keyIsPressed(key_state):
            if millis() >= self.end_time_:
               new_key = self.specialAction(spec_index)
               bitWrite(self.key_action_needed_map_, spec_index, 0)
            
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

            bitWrite(self.pressed_map_, spec_index, 0)
            bitWrite(self.key_action_needed_map_, spec_index, 0)

         return new_key

      if (self.pressed_map_ == 0):
         return mapped_key

      pressAllSpecials(row, col)
      self.key_action_needed_map_ = 0

      if (pressed_map_ > (1 << 7)):
         mapped_key = Layer.lookup(row, col)

      return mapped_key

dualUse = DualUse()

Kaleidoscope_.useEventHandlerHook(dualUse)

test = Test()
test.debug = True

test.addPermanentReportAssertions([DumpReport()])

test.keyDown(0, 1)
test.keyDown(0, 2)

test.queueGroupedReportAssertions([ 
      ReportKeyActive(key2())
   ])

test.scanCycle()

test.queueGroupedReportAssertions([ 
      ReportKeyActive(key2()),
      ReportModifierActive(keyLeftControl())
   ])
test.scanCycle()

test.log("Pressing key ...")
test.keyUp(0, 2)
test.keyUp(0, 1)

#TODO: Assert report empty (own assertion)

#test.queueGroupedReportAssertions([ 
   #TODO: Add no_keys_active and no_modifiers_active assertions
   #])
test.scanCycle()

test.keyDown(0, 1)
# TODO: Assert no key report. Due to debouncing?
test.scanCycle()


test.queueGroupedReportAssertions([ 
      ReportKeyActive(key1()),
      ReportModifierInactive(keyLeftControl())
   ])
test.scanCycle()
test.keyUp(0, 1)

#test.queueGroupedReportAssertions([ 
   #TODO: Add no_keys_active and no_modifiers_active assertions
   #])
test.scanCycle()
