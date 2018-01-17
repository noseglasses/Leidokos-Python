# -*- coding: utf-8 -*-
# -*- mode: Python -*-
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
#
# For documentation style see http://www.sphinx-doc.org/en/stable/ext/napoleon.html

import kaleidoscope
from kaleidoscope import *
from _Assertion import _Assertion

class ReportKeyActive(_Assertion):
   """ Asserts that a specific key is active in the keyboard report.
   
      Args:
         key (Key): The key tested for being active.
   """
   
   def __init__(self, key):
      _Assertion.__init__(self)
      self.key = key
      
   def _description(self):
      return "Key %s active" % str(kaleidoscope.keyToName(self.key))

   def _evalInternal(self, keyReport):
      return keyReport.isKeyActive(self.key)
   
class ReportKeyInactive(_Assertion):
   """ Asserts that a specific key is inactive in the keyboard report.
   
      Args:
         key (Key): The key tested for being inactive.
   """
   
   def __init__(self, key):
      _Assertion.__init__(self)
      self.key = key
      
   def _description(self):
      return "Key %s inactive" % str(kaleidoscope.Key.keyToName(self.key))

   def _evalInternal(self, keyReport):
      return not keyReport.isKeyActive(self.key)
   
class ReportKeycodeActive(_Assertion):
   """ Asserts that a specific keycode is active in the keyboard report.
   
      Args:
         keycode (int): The keycode tested for being active.
   """
   
   def __init__(self, keycode):
      _Assertion.__init__(self)
      self.keycode = keycode
      
   def _description(self):
      return "Keycode %s active" % str(kaleidoscope.Key.keycodeToName(self.keycode))

   def _evalInternal(self, keyReport):
      return keyReport.isKeycodeActive(self.keycode)
   
class ReportKeycodeInactive(_Assertion):
   """ Asserts that a specific key is inactive in the keyboard report.
   
      Args:
         keycode (int): The key tested for being inactive.
   """
   
   def __init__(self, keycode):
      _Assertion.__init__(self)
      self.keycode = keycode
      
   def _description(self):
      return "Keycode %s inactive" % str(kaleidoscope.Key.keycodeToName(self.keycode))

   def _evalInternal(self, keyReport):
      return not keyReport.isKeycodeActive(self.keycode)
   
class ReportKeysActive(_Assertion):
   """ Asserts that a specific list of keys is active in the keyboard report.
   
      Args:
         keys (list): A list of keys tested for being active.
         exclusively (boolean): It True, no other keycodes than the ones supplied 
                          are tolerated active.
   """
   
   def __init__(self, keys, exclusively = True):
      _Assertion.__init__(self)
      self.keys = keys
      self.exclusively = exclusively
      
   def _description(self):
      return "Keys active (%s)" % " ".join("'%s\'" % kaleidoscope.keyToName(x) for x in self.keys)

   def _evalInternal(self, keyReport):
      
      activeKeycodes = keyReport.getActiveKeycodes()
      
      for key in self.keys:
         if key.keyCode not in activeKeycodes:
            return False
      
      if self.exclusively:
         if len(activeKeycodes) != len(self.keys):
            return False
         
      return True
   
class ReportModifierActive(_Assertion):
   """ Asserts that a specific modifier is active in the keyboard report.
   
      Args:
         modifier (int): The modifier tested for being active.
   """
   
   def __init__(self, modifier):
      _Assertion.__init__(self)
      self.modifier = modifier
      
   def _description(self):
      return "Modifier %s active" % str(kaleidoscope.modifierKeyToName(self.modifier))

   def _evalInternal(self, keyReport):
      return keyReport.isModifierActive(self.modifier)
   
class ReportModifierInactive(_Assertion):
   """ Asserts that a specific modifier is inactive in the keyboard report.
   
      Args:
         modifier (int): The modifier tested for being inactive.
   """
   
   def __init__(self, modifier):
      _Assertion.__init__(self)
      self.modifier = modifier
      
   def _description(self):
      return "Modifier %s inactive" % str(kaleidoscope.modifierKeyToName(self.modifier))

   def _evalInternal(self, keyReport):
      return not keyReport.isModifierActive(self.modifier)
   
class ReportAnyModifiersActive(_Assertion):
   """ Asserts that any modifiers are active in a key report.
   """
      
   def _description(self):
      return "Any modifiers active"

   def _evalInternal(self, keyReport):
      return keyReport.isAnyModifierActive()
   
class ReportAllModifiersInactive(_Assertion):
   """ Asserts that all modifiers are inactive in a key report.
   """
      
   def _description(self):
      return "All modifiers inactive"

   def _evalInternal(self, keyReport):
      return not keyReport.isAnyModifierActive()
   
class ReportModifiersActive(_Assertion):
   """ Asserts that a specific list of modifiers is active in the keyboard report.
   
      Args:
         modifierKeys (list): A list of modifiers keys tested for being active.
         exclusively (boolean): It True, no other modifiers than the ones supplied 
                          are tolerated active.
   """
   
   def __init__(self, modifierKeys, exclusively = True):
      _Assertion.__init__(self)
      self.modifierKeys = modifierKeys
      self.exclusively = exclusively
      
   def _description(self):
      return "Modifiers active (%s)" % " ".join(kaleidoscope.modifierKeyToName(x) for x in self.modifierKeys)

   def _evalInternal(self, keyReport):
      
      activeModifiers = keyReport.getActiveModifiers()
      
      for mod in self.modifierKeys:
         if mod.keyCode not in activeModifiers:
            return False
      
      if self.exclusively:
         if len(activeModifiers) != len(self.modifierKeys):
            return False
         
      return True
   
class ReportAnyKeysActive(_Assertion):
   """ Asserts that any keys are active in a key report.
   """
      
   def _description(self):
      return "Any keys active"

   def _evalInternal(self, keyReport):
      return keyReport.isAnyKeyActive()
   
class ReportAllKeysInactive(_Assertion):
   """ Asserts that all keys are inactive in a key report.
   """
      
   def _description(self):
      return "All keys inactive"

   def _evalInternal(self, keyReport):
      return not keyReport.isAnyKeyActive()
   
class ReportEmpty(_Assertion):
   """ Asserts that a key report is empty.
   """
      
   def _description(self):
      return "Report empty"

   def _evalInternal(self, keyReport):
      return keyReport.isEmpty()
   
class ReportNotEmpty(_Assertion):
   """ Asserts that a key report is notempty.
   """
      
   def _description(self):
      return "Report not empty"

   def _evalInternal(self, keyReport):
      return not keyReport.isEmpty()
   
class ReportNthInCycle(_Assertion):
   """ Asserts that a report is the nth in its current cycle.
   
      Args:
         n (int): The report count.
   """
   
   def __init__(self, n):
      _Assertion.__init__(self)
      self.n = n
   
   def _description(self):
      return "Is %d. report in cycle" % self.n

   def _evalInternal(self, keyReport):
      return self._getTestDriver().nReportsInCycle == self.n
   
   def _actualState(self):
      return "%d. report in cycle" % self._getTestDriver().nReportsInCycle
   
class DumpReport(_Assertion):
   """ Dumps the current keyboard report. """
   
   def _evalInternal(self, keyReport):
      self.keyReport = keyReport
      return True
   
   def _description(self):
      return "Dump report: %s" % self.keyReport.dump()