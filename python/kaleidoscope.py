# -*- coding: utf-8 -*-
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
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import _kaleidoscope
from _kaleidoscope import *
import sys
import weakref
import os
import random
import operator

# For documentation style see http://www.sphinx-doc.org/en/stable/ext/napoleon.html

nIndentChars = 3
cycleIndent = " "*nIndentChars
keyboardReportIndent = " "*(nIndentChars*2)
assertionGroupIndent = " "*(nIndentChars*3)
assertionIndent = " "*(nIndentChars*4)

#class Key(_kaleidoscope.Key): pass

#class Layer(_kaleidoscope.Layer): pass

hidCodeToString = {
   0x04 : u"A", # HID_KEYBOARD_A_AND_A
   0x05 : u"B", # HID_KEYBOARD_B_AND_B
   0x06 : u"C", # HID_KEYBOARD_C_AND_C
   0x07 : u"D", # HID_KEYBOARD_D_AND_D
   0x08 : u"E", # HID_KEYBOARD_E_AND_E
   0x09 : u"F", # HID_KEYBOARD_F_AND_F
   0x0A : u"G", # HID_KEYBOARD_G_AND_G
   0x0B : u"H", # HID_KEYBOARD_H_AND_H
   0x0C : u"I", # HID_KEYBOARD_I_AND_I
   0x0D : u"J", # HID_KEYBOARD_J_AND_J
   0x0E : u"K", # HID_KEYBOARD_K_AND_K
   0x0F : u"L", # HID_KEYBOARD_L_AND_L
   0x10 : u"M", # HID_KEYBOARD_M_AND_M
   0x11 : u"N", # HID_KEYBOARD_N_AND_N
   0x12 : u"O", # HID_KEYBOARD_O_AND_O
   0x13 : u"P", # HID_KEYBOARD_P_AND_P
   0x14 : u"Q", # HID_KEYBOARD_Q_AND_Q
   0x15 : u"R", # HID_KEYBOARD_R_AND_R
   0x16 : u"S", # HID_KEYBOARD_S_AND_S
   0x17 : u"T", # HID_KEYBOARD_T_AND_T
   0x18 : u"U", # HID_KEYBOARD_U_AND_U
   0x19 : u"V", # HID_KEYBOARD_V_AND_V
   0x1A : u"W", # HID_KEYBOARD_W_AND_W
   0x1B : u"X", # HID_KEYBOARD_X_AND_X
   0x1C : u"Y", # HID_KEYBOARD_Y_AND_Y
   0x1D : u"Z", # HID_KEYBOARD_Z_AND_Z
   0x1E : u"1 !", # HID_KEYBOARD_1_AND_EXCLAMATION_POINT
   0x1F : u"2 @", # HID_KEYBOARD_2_AND_AT
   0x20 : u"3 #", # HID_KEYBOARD_3_AND_POUND
   0x21 : u"4 $", # HID_KEYBOARD_4_AND_DOLLAR
   0x22 : u"5 %", # HID_KEYBOARD_5_AND_PERCENT
   0x23 : u"6 ^", # HID_KEYBOARD_6_AND_CARAT
   0x24 : u"7 &", # HID_KEYBOARD_7_AND_AMPERSAND
   0x25 : u"8 *", # HID_KEYBOARD_8_AND_ASTERISK
   0x26 : u"9 (", # HID_KEYBOARD_9_AND_LEFT_PAREN
   0x27 : u"0 )", # HID_KEYBOARD_0_AND_RIGHT_PAREN
   0x28 : "\u23CE", # HID_KEYBOARD_ENTER	0x28	 // (MARKED AS ENTER_SLASH_RETURN)
   0x29 : u"Esc", # HID_KEYBOARD_ESCAPE
   0x2A : u"Del", # HID_KEYBOARD_DELETE	0x2A	// (BACKSPACE)
   0x2B : u"Tab", # HID_KEYBOARD_TAB
   0x2C : u"\u0020", # HID_KEYBOARD_SPACEBAR
   0x2D : u"- _", # HID_KEYBOARD_MINUS_AND_UNDERSCORE	0x2D	 // (UNDERSCORE)
   0x2E : u"= +", # HID_KEYBOARD_EQUALS_AND_PLUS
   0x2F : u"[ {", # HID_KEYBOARD_LEFT_BRACKET_AND_LEFT_CURLY_BRACE
   0x30 : u"] }", # HID_KEYBOARD_RIGHT_BRACKET_AND_RIGHT_CURLY_BRACE
   0x31 : u"\ |", # HID_KEYBOARD_BACKSLASH_AND_PIPE
   0x32 : u"~", # HID_KEYBOARD_NON_US_POUND_AND_TILDE
   0x33 : u"; :", # HID_KEYBOARD_SEMICOLON_AND_COLON
   0x34 : u"\' \"", # HID_KEYBOARD_QUOTE_AND_DOUBLEQUOTE
   0x35 : u"` ~", # HID_KEYBOARD_GRAVE_ACCENT_AND_TILDE
   0x36 : u", <", # HID_KEYBOARD_COMMA_AND_LESS_THAN
   0x37 : u". >", # HID_KEYBOARD_PERIOD_AND_GREATER_THAN
   0x38 : u"/ ?", # HID_KEYBOARD_SLASH_AND_QUESTION_MARK
   0x39 : u"C.L.", # HID_KEYBOARD_CAPS_LOCK
   0x3A : u"F1", # HID_KEYBOARD_F1
   0x3B : u"F2", # HID_KEYBOARD_F2
   0x3C : u"F3", # HID_KEYBOARD_F3
   0x3D : u"F4", # HID_KEYBOARD_F4
   0x3E : u"F5", # HID_KEYBOARD_F5
   0x3F : u"F6", # HID_KEYBOARD_F6
   0x40 : u"F7", # HID_KEYBOARD_F7
   0x41 : u"F8", # HID_KEYBOARD_F8
   0x42 : u"F9", # HID_KEYBOARD_F9
   0x43 : u"F10", # HID_KEYBOARD_F10
   0x44 : u"F11", # HID_KEYBOARD_F11
   0x45 : u"F12", # HID_KEYBOARD_F12
   0x46 : u"PRTS", # HID_KEYBOARD_PRINTSCREEN
   0x47 : u"ScLk", # HID_KEYBOARD_SCROLL_LOCK
   0x48 : u"Pse", # HID_KEYBOARD_PAUSE
   0x49 : u"Isrt", # HID_KEYBOARD_INSERT
   0x4A : u"Home", # HID_KEYBOARD_HOME
   0x4B : u"PgUp", # HID_KEYBOARD_PAGE_UP
   0x4C : u"Del", # HID_KEYBOARD_DELETE_FORWARD
   0x4D : u"End", # HID_KEYBOARD_END
   0x4E : u"PgDn", # HID_KEYBOARD_PAGE_DOWN
   0x4F : u"→", # HID_KEYBOARD_RIGHT_ARROW
   0x50 : u"←", # HID_KEYBOARD_LEFT_ARROW
   0x51 : u"↓", # HID_KEYBOARD_DOWN_ARROW
   0x52 : u"↑", # HID_KEYBOARD_UP_ARROW
   0x53 : u"NlCl", # HID_KEYPAD_NUM_LOCK_AND_CLEAR
   0x54 : u"/", # HID_KEYPAD_DIVIDE
   0x55 : u"*", # HID_KEYPAD_MULTIPLY
   0x56 : u"-", # HID_KEYPAD_SUBTRACT
   0x57 : u"+", # HID_KEYPAD_ADD
   0x58 : u"Entr", # HID_KEYPAD_ENTER
   0x59 : u"1 Ed", # HID_KEYPAD_1_AND_END
   0x5A : u"2 ↓", # HID_KEYPAD_2_AND_DOWN_ARROW
   0x5B : u"3 PD", # HID_KEYPAD_3_AND_PAGE_DOWN
   0x5C : u"4 ←", # HID_KEYPAD_4_AND_LEFT_ARROW
   0x5D : u"5", # HID_KEYPAD_5
   0x5E : u"6 →", # HID_KEYPAD_6_AND_RIGHT_ARROW
   0x5F : u"7 Hm", # HID_KEYPAD_7_AND_HOME
   0x60 : u"8 ↑", # HID_KEYPAD_8_AND_UP_ARROW
   0x61 : u"9 PU", # HID_KEYPAD_9_AND_PAGE_UP
   0x62 : u"0 IN", # HID_KEYPAD_0_AND_INSERT
   0x63 : u". DL", # HID_KEYPAD_PERIOD_AND_DELETE
   0x64 : u"\ |", # HID_KEYBOARD_NON_US_BACKSLASH_AND_PIPE
   #0x65 : # HID_KEYBOARD_APPLICATION
   #0x66 : # HID_KEYBOARD_POWER
   0x67 : u"=", # HID_KEYPAD_EQUALS
   0x68 : u"F13", # HID_KEYBOARD_F13
   0x69 : u"F14", # HID_KEYBOARD_F14
   0x6A : u"F15", # HID_KEYBOARD_F15
   0x6B : u"F16", # HID_KEYBOARD_F16
   0x6C : u"F17", # HID_KEYBOARD_F17
   0x6D : u"F18", # HID_KEYBOARD_F18
   0x6E : u"F19", # HID_KEYBOARD_F19
   0x6F : u"F20", # HID_KEYBOARD_F20
   0x70 : u"F21", # HID_KEYBOARD_F21
   0x71 : u"F22", # HID_KEYBOARD_F22
   0x72 : u"F23", # HID_KEYBOARD_F23
   0x73 : u"F24", # HID_KEYBOARD_F24
   #0x74 :  , # HID_KEYBOARD_EXECUTE
   #0x75 :  , # HID_KEYBOARD_HELP
   #0x76 :  , # HID_KEYBOARD_MENU
   #0x77 :  , # HID_KEYBOARD_SELECT
   #0x78 :  , # HID_KEYBOARD_STOP
   #0x79 :  , # HID_KEYBOARD_AGAIN
   #0x7A :  , # HID_KEYBOARD_UNDO
   #0x7B :  , # HID_KEYBOARD_CUT
   #0x7C :  , # HID_KEYBOARD_COPY
   #0x7D :  , # HID_KEYBOARD_PASTE
   #0x7E :  , # HID_KEYBOARD_FIND
   #0x7F :  , # HID_KEYBOARD_MUTE
   #0x80 :  , # HID_KEYBOARD_VOLUME_UP
   #0x81 :  , # HID_KEYBOARD_VOLUME_DOWN
   #0x82 :  , # HID_KEYBOARD_LOCKING_CAPS_LOCK
   #0x83 :  , # HID_KEYBOARD_LOCKING_NUM_LOCK
   #0x84 :  , # HID_KEYBOARD_LOCKING_SCROLL_LOCK
   0x85 : u",", # HID_KEYPAD_COMMA
   0x86 : u"=", # HID_KEYPAD_EQUAL_SIGN
}

def _removeItemsFromList(fromList, removalList):
   """ Removes all items from a list.
   
   Args:
      fromList (list): The list to remove entries from.
      removalList (list): The list that contains the entries to remove.
      
   Returns:
      list: Copy of fromList with items removed.
   """
   return [assertion for assertion in fromList if assertion not in removalList]

class Assertion(object):
   """ The base class of all assertions """
   
   def __init__(self):
      self.typeKeyword = ""
   
   def _report(self, out):
      
      """ Generates a verbose report of the assertion.
      
      Args:
         out (stream): A stream object that features a write(...) method.
      """
      if self.valid:
         out.write("%s assertion passed: %s\n" % (self.typeKeyword, self._description()), assertionIndent)
      else:
         out.write("!!! %s assertion failed: %s\n" % (self.typeKeyword, self._description()), assertionIndent)
         theActualState = self._actualState()
         if theActualState:
            out.write("   actual: %s\n" % theActualState, assertionIndent)
            
   def _description(self):
      """ Returns a description string. """
        
   def _evalInternal(self, target):
      """ The internal assertion evaluation method. This method may be overridden
         by derived assertion classes.
      
      Args:
         target (undefined): The target object the assertion operates on.
            This can either be a KeyboardReport object, the Test object or others.
            
      Returns:
         bool: True if the assertion passed, False otherwise.
      """
      return True
      
   def _eval(self, target):
      """ The main assertion evaluation method. Do not override this method
         but _evalInternal(...) instead.
      
      Args:
         target (undefined): The target object the assertion operates on.
            This can either be a KeyboardReport object, the Test object or others.
            
      Returns:
         bool: True if the assertion passed, False otherwise.
      """
      
      if not self._evalInternal(target):
         self.valid = False
         return False
      
      self.valid = True
      return True
   
   def _actualState(self):
      """ Writes the actual state of the assertion to self.out.
         This method can be overridden.
      """
      return None

   def _setTest(self, test):
      """ Sets the associated Test object. """
      self.testWeak = weakref.ref(test)

   def _getTest(self):
      """ Returns a reference to the associated test object. """
      return self.testWeak()
   
class AssertionGroup(Assertion):
   """ Groups several assertions.
   
      Args:
         assertionList (list): A list of assertions.
   """

   def __init__(self, assertionList):
      Assertion.__init__(self)
      self.assertionList = assertionList
   
   def _report(self, out):
      """ Generates a report by letting all members report. """
      for assertion in self.assertionList:
         assertion._report(out) 
         
   def _evalInternal(self, keyReport):
      
      self.valid = True
      for assertion in self.assertionList:
         self.valid &= assertion._eval(keyReport)
         
      return self.valid
   
   def _setTest(self, test):
      for assertion in self.assertionList:
         assertion._setTest(test)

################################################################################
# Key report assertions
################################################################################

class ReportKeyActive(Assertion):
   """ Asserts that a specific key is active in the keyboard report.
   
      Args:
         key (Key): The key tested for being active.
   """
   
   def __init__(self, key):
      Assertion.__init__(self)
      self.key = key
      
   def _description(self):
      return "Key %s active" % str(_kaleidoscope.keyToName(self.key))

   def _evalInternal(self, keyReport):
      return keyReport.isKeyActive(self.key)
   
class ReportKeyInactive(Assertion):
   """ Asserts that a specific key is inactive in the keyboard report.
   
      Args:
         key (Key): The key tested for being inactive.
   """
   
   def __init__(self, key):
      Assertion.__init__(self)
      self.key = key
      
   def _description(self):
      return "Key %s inactive" % str(_kaleidoscope.Key.keyToName(self.key))

   def _evalInternal(self, keyReport):
      return not keyReport.isKeyActive(self.key)
   
class ReportKeycodeActive(Assertion):
   """ Asserts that a specific keycode is active in the keyboard report.
   
      Args:
         keycode (int): The keycode tested for being active.
   """
   
   def __init__(self, keycode):
      Assertion.__init__(self)
      self.keycode = keycode
      
   def _description(self):
      return "Keycode %s active" % str(_kaleidoscope.Key.keycodeToName(self.keycode))

   def _evalInternal(self, keyReport):
      return keyReport.isKeycodeActive(self.keycode)
   
class ReportKeycodeInactive(Assertion):
   """ Asserts that a specific key is inactive in the keyboard report.
   
      Args:
         keycode (int): The key tested for being inactive.
   """
   
   def __init__(self, keycode):
      Assertion.__init__(self)
      self.keycode = keycode
      
   def _description(self):
      return "Keycode %s inactive" % str(_kaleidoscope.Key.keycodeToName(self.keycode))

   def _evalInternal(self, keyReport):
      return not keyReport.isKeycodeActive(self.keycode)
   
class ReportKeysActive(Assertion):
   """ Asserts that a specific list of keys is active in the keyboard report.
   
      Args:
         keys (list): A list of keys tested for being active.
         exclusively (boolean): It True, no other keycodes than the ones supplied 
                          are tolerated active.
   """
   
   def __init__(self, keys, exclusively = True):
      Assertion.__init__(self)
      self.keys = keys
      self.exclusively = exclusively
      
   def _description(self):
      return "Keys active (%s)" % " ".join("'%s\'" % _kaleidoscope.keyToName(x) for x in self.keys)

   def _evalInternal(self, keyReport):
      
      activeKeycodes = keyReport.getActiveKeycodes()
      
      for key in self.keys:
         if key.keyCode not in activeKeycodes:
            return False
      
      if self.exclusively:
         if len(activeKeycodes) != len(self.keys):
            return False
         
      return True
   
class ReportModifierActive(Assertion):
   """ Asserts that a specific modifier is active in the keyboard report.
   
      Args:
         modifier (int): The modifier tested for being active.
   """
   
   def __init__(self, modifier):
      Assertion.__init__(self)
      self.modifier = modifier
      
   def _description(self):
      return "Modifier %s active" % str(_kaleidoscope.modifierKeyToName(self.modifier))

   def _evalInternal(self, keyReport):
      return keyReport.isModifierActive(self.modifier)
   
class ReportModifierInactive(Assertion):
   """ Asserts that a specific modifier is inactive in the keyboard report.
   
      Args:
         modifier (int): The modifier tested for being inactive.
   """
   
   def __init__(self, modifier):
      Assertion.__init__(self)
      self.modifier = modifier
      
   def _description(self):
      return "Modifier %s inactive" % str(_kaleidoscope.modifierKeyToName(self.modifier))

   def _evalInternal(self, keyReport):
      return not keyReport.isModifierActive(self.modifier)
   
class ReportAnyModifiersActive(Assertion):
   """ Asserts that any modifiers are active in a key report.
   """
      
   def _description(self):
      return "Any modifiers active"

   def _evalInternal(self, keyReport):
      return keyReport.isAnyModifierActive()
   
class ReportAllModifiersInactive(Assertion):
   """ Asserts that all modifiers are inactive in a key report.
   """
      
   def _description(self):
      return "All modifiers inactive"

   def _evalInternal(self, keyReport):
      return not keyReport.isAnyModifierActive()
   
class ReportModifiersActive(Assertion):
   """ Asserts that a specific list of modifiers is active in the keyboard report.
   
      Args:
         modifierKeys (list): A list of modifiers keys tested for being active.
         exclusively (boolean): It True, no other modifiers than the ones supplied 
                          are tolerated active.
   """
   
   def __init__(self, modifierKeys, exclusively = True):
      Assertion.__init__(self)
      self.modifierKeys = modifierKeys
      self.exclusively = exclusively
      
   def _description(self):
      return "Modifiers active (%s)" % " ".join(_kaleidoscope.modifierKeyToName(x) for x in self.modifierKeys)

   def _evalInternal(self, keyReport):
      
      activeModifiers = keyReport.getActiveModifiers()
      
      for mod in self.modifierKeys:
         if mod.keyCode not in activeModifiers:
            return False
      
      if self.exclusively:
         if len(activeModifiers) != len(self.keycodes):
            return False
         
      return True
   
class ReportAnyKeysActive(Assertion):
   """ Asserts that any keys are active in a key report.
   """
      
   def _description(self):
      return "Any keys active"

   def _evalInternal(self, keyReport):
      return keyReport.isAnyKeyActive()
   
class ReportAllKeysInactive(Assertion):
   """ Asserts that all keys are inactive in a key report.
   """
      
   def _description(self):
      return "All keys inactive"

   def _evalInternal(self, keyReport):
      return not keyReport.isAnyKeyActive()
   
class ReportEmpty(Assertion):
   """ Asserts that a key report is empty.
   """
      
   def _description(self):
      return "Report empty"

   def _evalInternal(self, keyReport):
      return keyReport.isEmpty()
   
class ReportNotEmpty(Assertion):
   """ Asserts that a key report is notempty.
   """
      
   def _description(self):
      return "Report not empty"

   def _evalInternal(self, keyReport):
      return not keyReport.isEmpty()
   
class ReportNthInCycle(Assertion):
   """ Asserts that a report is the nth in its current cycle.
   
      Args:
         n (int): The report count.
   """
   
   def __init__(self, n):
      Assertion.__init__(self)
      self.n = n
   
   def _description(self):
      return "Is %d. report in cycle" % self.n

   def _evalInternal(self, keyReport):
      return self._getTest().nReportsInCycle == self.n
   
   def _actualState(self):
      return "%d. report in cycle" % self._getTest().nReportsInCycle
   
class ReportNthCycle(Assertion):
   """ Asserts that the current cycle is the nth.
   
      Args:
         cycle (int): The cycle count.
   """
   
   def __init__(self, cycle):
      Assertion.__init__(self)
      self.cycle = cycle
   
   def _description(self):
      return "Is %d. cycle" % self.cycle

   def _actualState(self):
      return "%d. cycle" % self._getTest().cycleId
   
   def _evalInternal(self, dummy):
      return self._getTest().cycleId == self.cycle
   
class DumpReport(Assertion):
   """ Dumps the current keyboard report. """
   
   def _evalInternal(self, keyReport):
      self.keyReport = keyReport
      return True
   
   def _description(self):
      return "Dump report: %s" % self.keyReport.dump()
         
################################################################################
# General assertions
################################################################################

class CycleHasNReports(Assertion):
   """ Asserts that there was a specific number of keyboard reports generated
      within a cycle.
      
      Args:
         nReports (int): The required number of reports.
   """
   
   def __init__(self, nReports):
      Assertion.__init__(self)
      self.nReports = nReports
   
   def _description(self):
      return "There were %d keyboard reports in cycle" % self.nReports

   def _actualState(self):
      return "%d keyboard reports" % self._getTest().nReportsInCycle
   
   def _evalInternal(self, dummy):
      return self._getTest().nReportsInCycle == self.nReports
   
class CycleIsNth(ReportNthCycle):
   """ Asserts that the current cycle is the nth.
   
      Args:
         cycle (int): The cycle count.
   """
   pass

class LayerIsActive(Assertion):
   """ Asserts that a given layer is active (the current top layer).
      
      Args:
         layer (int): The id of the required layer.
   """
   
   def __init__(self, layer):
      Assertion.__init__(self)
      self.layer = layer
   
   def _description(self):
      return "Is %d. layer active" % self.layer

   def _actualState(self):
      return "%d. layer is active" % _kaleidoscope.Layer.top()
   
   def _evalInternal(self, dummy):
      return _kaleidoscope.top() == self.layer
   
class LayerIsInactive(Assertion):
   """ Asserts that a given layer is currently not active (not the current top layer).
      
      Args:
         layer (int): The id of the layer required to be not active.
   """
   
   def __init__(self, layer):
      Assertion.__init__(self)
      self.layer = layer
   
   def _description(self):
      return "Is %d. layer inactive" % self.layer

   def _actualState(self):
      return "%d. layer is active" % _kaleidoscope.Layer.top()
   
   def _evalInternal(self, dummy):
      return _kaleidoscope.top() != self.layer
   
class TimeElapsedGreater(Assertion):
   """ Asserts that that time that elapsed is greater than a given time in [ms].
      
      Args:
         startT (float): The reference start time.
         deltaT (float): The time in [ms] that is required to have elapsed.
   """
   
   def __init__(self, startT, deltaT):
      Assertion.__init__(self)
      self.startT = startT
      self.deltaT  = deltaT 
   
   def _description(self):
      return "Time elapsed greater %f ms" % self.layer

   def _actualState(self):
      return "Time elapsed is %f ms" % (test.time - self.startT)
   
   def _evalInternal(self, dummy):
      return test.time - self.startT > self.deltaT
   
################################################################################
# Main test class
################################################################################
   
class _KeyboardReportCallbackProxy(object):
   
   def __init__(self, test):
      self.testWeak = weakref.ref(test)
   
   def processReport(self, keyboardReport):
      self.testWeak()._processReport(keyboardReport)
      
class _TimedStream(object):
   
   def __init__(self, test, out):
      self.testWeak = weakref.ref(test)
      self.out = out
      self.indentChars = 3
      
   def write(self, string, indentationString = "", outputTime = True):
      if outputTime:
         timeStr = ""
         if(self.testWeak()):
            timeStr = "%010d " % self.testWeak().time
         self.out.write("%s%s%s" % (timeStr, indentationString, string))
      else:
         self.out.write("%s%s" % (indentationString, string))
         
   def writeN(self, string, indentationString = ""):
      self.write(string, indentationString, outputTime = False)
   
class Test(object):
   """ The main test object that controls everything.
   
   Attributes:
      out (stream): A stream that should be used for all output using write(...).
      
      debug (bool): Additional output is generated when set to True. Defaults to False.
   """
   def __init__(self, 
                out = sys.stdout, 
                debug = False, 
                cycleDuration = 5):
      
      self.assertionsPassed = True
      self.nReportsInCycle = 0
      self.nKeyboardReports = 0
      
      # The cycle duration in ms
      #
      self.cycleDuration = cycleDuration
      self.cycleId = 0
      self.time = 0
      
      # The preferred output
      #
      self.out = _TimedStream(self, out)
      
      self.queuedReportAssertions = []
      self.permanentReportAssertions = []
      self.queuedCycleAssertions = []
      self.permanentCycleAssertions = []
      
      self.debug = debug
      
      _kaleidoscope.setKeyboardReportCallback(_KeyboardReportCallbackProxy(self))
   
      _kaleidoscope.init()
      
      self._headerText()
      
      try:
         __NO_EXIT__
      except NameError:
         self.noExit = True
      else:
         self.noExit = False
      
   def __del__(self):
      
      _kaleidoscope.finalize()
      
      self._footerText()
      
      if not self._checkStatus():
         self._error("Terminating with exit code 1")
         
   def setOutputStream(self, out):
      """ Sets an output stream that is used for all formatted output.
      
      Args:
         out (stream): An output stream.
      """
      self.out = _TimedStream(self, out)
         
   def _error(self, msg):
      self.out.writeN("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
      self.out.writeN("!!! Error: %s\n" % msg)
      self.out.writeN("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        
      if not self.noExit:
         os._exit(1)
      
   def _headerText(self):
      self.out.writeN("\n")
      self.out.writeN("################################################################################\n")
      self.out.writeN("\n")
      self.out.writeN("Kaleidoscope-Python\n")
      self.out.writeN("\n")
      self.out.writeN("author: noseglasses (https://github.com/noseglasses, shinynoseglasses@gmail.com)\n")
      self.out.writeN("version: %s\n" % _kaleidoscope.getVersionString())
      self.out.writeN("\n")
      self.out.writeN("cycle duration: %f\n" % self.cycleDuration)
      self.out.writeN("################################################################################\n")
      self.out.writeN("\n")
      
   def _footerText(self):
      self.out.writeN("\n")
      self.out.writeN("################################################################################\n")
      self.out.writeN("Testing done\n")
      self.out.writeN("################################################################################\n")
      self.out.writeN("\n")
      
   def _checkStatus(self):
      success = True
      if len(self.queuedReportAssertions) > 0:
         self.out.write("!!! Error: There are %d left over assertions in the queue\n" % len(self.queuedReportAssertions))
         success = False
      
      if not self.assertionsPassed:
         self.out.write("!!! Error: Not all assertions passed\n")
         success = False
         
      if success:
         self.out.write("All tests passed.\n")
         return True
      
      return False

   def _configureReportAssertions(self, assertionList):
      for assertion in assertionList:
         self._configureReportAssertion(assertion)
         
   def _configureReportAssertion(self, assertion):
      assertion._setTest(self)
      assertion.typeKeyword = "Report"
      
   def queueReportAssertion(self, assertion):
      """ Queues a report assertions. The report assertion at the end of 
      the queue will be cast on the next key report. Then the respective 
      assertion will be discarded.
      
      Args:
         assertion (Assertion): The assertion to add to the queue.
      """
      self._configureReportAssertion(assertion)
      self.queuedReportAssertions.append(assertion)
      
   def _generateAssertionGroup(self, assertionList):
      for assertion in assertionList:
         self._configureReportAssertion(assertion)
      assertionGroup = AssertionGroup(assertionList)
      self._configureReportAssertion(assertionGroup)
      return assertionGroup
      
   def queueGroupedReportAssertions(self, assertionList):
      """ Queues a number of report assertions. The assertions will be 
      grouped and cast together on a key report. Once casted they will
      all be discarded.
      
      Args:
         assertionList (list): A list of assertions to group and queue.
      """
      self.queuedReportAssertions.append(
         self._generateAssertionGroup(assertionList))
      
   def removeQueuedReportAssertions(self, assertionList):
      """ Removes assertions from the report assertion queue (only if registered). 
      Assertions that are not registered are ignored.
      
      Args:
         assertionList (list): A list of assertions to be removed.
      """
      self.queuedReportAssertions = \
         _removeItemsFromList(self.queuedReportAssertions, assertionList)
      
   def addPermanentReportAssertion(self, assertion):
      """ Adds a permanent report assertion. The assertions thus added will
      be cast on every future keyboard report until removed.
      
      Args:
         assertion (Assertion): An assertions to be used permanently.
      """
      self._configureReportAssertion(assertion)
      self.permanentReportAssertions.append(assertion)
      
   def addPermanentReportAssertions(self, assertionList):
      """ Adds a number of permanent report assertions. The assertions thus added will
      be cast on every future keyboard report until removed.
      
      Args:
         assertionList (list): A list of assertions to be used permanently.
      """
      self._configureReportAssertions(assertionList)
      self.permanentReportAssertions.extend(assertionList)
      
   def removePermanentReportAssertions(self, assertionList):
      """ Removes a number of permanent report assertions (only if registered). 
      Assertions that are not registered are ignored.
      
      Args:
         assertionList (list): A list of assertions to be removed.
      """
      self.permanentReportAssertions = \
         _removeItemsFromList(self.permanentReportAssertions, assertionList)
      
   def removeReportAssertions(self, assertionList):
      """ Removes a number of report assertions from both queued and permanent 
      assertions (only if registered). Assertions that are not registered are ignored.
      
      Args:
         assertionList (list): A list of assertions to be removed.
      """
      self.removeQueuedReportAssertions(assertionList)
      self.removePermanentReportAssertions(assertionList)
      
   def _processReport(self, keyReport):
      
      self.nKeyboardReports += 1
         
      self.nReportsInCycle += 1
      
      self.out.write("Processing keyboard report %d (%d. in cycle)\n"
                     % (self.nKeyboardReports, self.nReportsInCycle), keyboardReportIndent)
      
      self.out.write("%d queued report assertions\n" % len(self.queuedReportAssertions), assertionGroupIndent)
      
      if len(self.queuedReportAssertions) > 0:
         self._processReportAssertion(self.queuedReportAssertions[0], keyReport)
         self.queuedReportAssertions.pop(0)
         
      if len(self.permanentReportAssertions) > 0:
         
         self.out.write("%d permanent report assertions\n" % len(self.permanentReportAssertions), assertionGroupIndent)
         for assertion in self.permanentReportAssertions:
            self._processReportAssertion(assertion, keyReport)
         
   def _processReportAssertion(self, assertion, keyReport):
      
      assertionPassed = assertion._eval(keyReport)
      
      if not assertionPassed or self.debug:
         assertion._report(self.out)
      
      self.assertionsPassed &= assertionPassed
         
   # Some wrapper functions for kaleidoscope stuff
   
   def keyDown(self, row, col):
      """ Registers a key down event.
      
      Args:
         row (int): The keyboard key row.
         col (int): The keyboard key col.
      """
      
      self.out.write("+ Activating key (%d, %d)\n" % (row, col))
      
      _kaleidoscope.keyDown(row, col)
      
   def keyUp(self, row, col):
      """ Registers a key up event. Make sure that the key was registered
      as active before, using keyDown(...).
      
      Args:
         row (int): The keyboard key row.
         col (int): The keyboard key col.
      """
      self.out.write("- Releasing key (%d, %d)\n" % (row, col))
      _kaleidoscope.keyUp(row, col)
   
   def tap(self, row, col):
      """ Registers tap of a key.
      
      Args:
         row (int): The keyboard key row.
         col (int): The keyboard key col.
      """
      _kaleidoscope.tap(row, col)

   def clearAllKeys(self):
      """ Clears all keys that are currently active (down). """
      self.out.write("- Clearing all keys\n")
      _kaleidoscope.clearAllKeys()
      
   def _configureCycleAssertion(self, assertion):
      assertion._setTest(self)
      assertion.typeKeyword = "Cycle"
      
   def _configureTemporaryAssertion(self, assertion):
      assertion._setTest(self)
      assertion.typeKeyword = "Temporary cycle"
      
   def queueCycleAssertions(self, assertionList):
      """ Queues a number of cycle assertions. Queued assertions will be 
      applied at the end of the next cycle and then discarded.
      
      Args:
         assertionList (list): A list of assertions to be queued.
      """
      for assertion in assertionList:
         self._configureReportAssertion(assertion)
      
      self.queuedCycleAssertions.extend(assertionList)
      
   def removeQueuedCycleAssertions(self, assertionList):
      """ Removes a number of queued cycle assertions (only if registered).
      Assertions that are not registered are ignored.
      
      Args:
         assertionList (list): A list of assertions to be removed.
      """
      self.queuedCycleAssertions = \
         _removeItemsFromList(self.queuedCycleAssertions, assertionList)
      
   def registerPermanentCycleAssertions(self, assertionList):
      """ Registers a number of cycle assertions that are 
      applied after every future cycle until removed.
      
      Args:
         assertionList (list): A list of assertions to be registered.
      """
      for assertion in assertionList:
         self._configureReportAssertion(assertion)
      
      self.permanentCycleAssertions.extend(assertionList)
      
   def removePermanentCycleAssertions(self, assertionList):
      """ Removes a number of permanent cycle assertions (only if registered).
      Assertions that are not registered are ignored.
      
      Args:
         assertionList (list): A list of assertions to be removed.
      """
      self.queuedCycleAssertions = \
         _removeItemsFromList(self.permanentCycleAssertions, assertionList)
      
   def removeCycleAssertions(self, assertionList):
      """ Removes a number of cycle assertions, both from queued
      and permanent assertions (only if registered).
      Assertions that are not registered are ignored.
      
      Args:
         assertionList (list): A list of assertions to be removed.
      """
      self.removeQueuedCycleAssertions(assertionList)
      self.removePermanentCycleAssertions(assertionList)
      
   def scanCycle(self, onStopAssertionList = None):
      """ Executes a scan cycle and processes assertions afterwards.
      
      Args:
         onStopAssertionList (list): A list of assertions to be executed after
            the next cycle and to be discarded afterwards. Defaults to None.
      """
      self.out.write("Running single scan cycle\n")
      self._scanCycle(onStopAssertionList)
      self.out.write("\n")
      
   def _scanCycle(self, onStopAssertionList = None):
      
      self.cycleId += 1
      self.nReportsInCycle = 0
      
      self.out.write("Scan cycle %d\n" % self.cycleId, cycleIndent)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            self._configureTemporaryAssertion(assertion)
      
      _kaleidoscope.scanCycle()
      
      if self.nReportsInCycle == 0:
         self.out.write("No keyboard reports processed\n", keyboardReportIndent)
      else:
         self.out.write("%d keyboard reports processed\n" % self.nReportsInCycle, keyboardReportIndent)
      
      self.time += self.cycleDuration
      
      _kaleidoscope.setMillis(self.time)
      
      if onStopAssertionList and len(onStopAssertionList) > 0:
         self.out.write("Processing %d cycle assertions on stop\n" % len(onStopAssertionList), assertionGroupIndent)
         self._processCycleAssertions(onStopAssertionList)
      
      if len(self.queuedCycleAssertions) > 0:
         self.out.write("Processing %d queued cycle assertions\n" % len(self.queuedCycleAssertions), assertionGroupIndent)
         self._processCycleAssertions(self.queuedCycleAssertions)
         
         self.queuedCycleAssertions = []
      
      if len(self.permanentCycleAssertions) > 0:
         self.out.write("Processing %d permanent cycle assertions\n" % len(self.permanentCycleAssertions), assertionGroupIndent)
         self._processCycleAssertions(self.permanentCycleAssertions)
      
   def scanCycles(self, n, onStopAssertionList = None, cycleAssertionList = None):
      """ Executes a number of scan cycles and processes assertions afterwards.
      
      Args:
         n (int): The number of cycles to execute.
         onStopAssertionList (list): A list of assertions to be executed after
            the cycles where executed and to be discarded afterwards. Defaults
            to None.
         cycleAssertionList (list): A list of assertions that are executed
            after every cycle.
      """
      
      self.out.write("Running %d scan cycles\n" % n)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            self._configureTemporaryAssertion(assertion)
            
      for i in range(0, n):
         self._scanCycle(cycleAssertionList)
         
      if onStopAssertionList and len(onStopAssertionList) > 0:
         self.out.write("Processing %d cycle assertions on stop\n" % len(onStopAssertionList), cycleIndent)
         self._processCycleAssertions(onStopAssertionList)
         
      self.out.write("\n")
         
   def skipTime(self, deltaT , onStopAssertionList = None):
      """ Skips a given amount of time by executing cycles and processes assertions afterwards.
      
      Important:
         Make sure to set the cycleDuration property of the Test class 
         to a non zero value in [ms] before calling this method.
      
      Args:
         deltaT (float): A time in [ms] that is supposed to be skipped.
         onStopAssertionList (list): A list of assertions to be executed after
            the cycles where executed and to be discarded afterwards. Defaults
            to None.
      """
      
      self._checkCycleDurationSet()
      
      startCycle = self.cycleId
      
      self.out.write("Skipping dt >= %f ms\n" % deltaT)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            assertion._setTest(self)
            
      startTime = self.time
      
      elapsedTime = 0
      while elapsedTime < deltaT:
         self._scanCycle()
         elapsedTime = self.time - startTime
         
      self.out.write("%f ms (%d cycles) skipped\n" % (elapsedTime, self.cycleId - startCycle), cycleIndent)
         
      if onStopAssertionList and len(onStopAssertionList) > 0:
         self.out.write("Processing %d cycle assertions on stop\n" % len(onStopAssertionList), cycleIndent)
         self._processCycleAssertions(onStopAssertionList)
         
      self.out.write("\n")
         
   def _checkCycleDurationSet(self):
      if self.cycleDuration == 0:
         self._error("Please set test.cycleDuration to a value in "
            "[ms] greater zero before using time based testing")
         
   def _processCycleAssertions(self, assertionList):
      
      if not assertionList:
         return
      
      if len(assertionList) == 0:
         return
      
      for assertion in assertionList:
         
         assertion._setTest(self)
         
         assertionPassed = assertion._eval(self)
         
         if not assertionPassed:
            assertion._report(self.out)
         elif self.debug:
            assertion._report(self.out)
         
         self.assertionsPassed &= assertionPassed
         
   def log(self, msg):
      """ Writes a log message.
      
      Args:
         msg (string): The log message.
      """
      self.out.write("~ %s ~\n" % msg)
   
   def header(self, msg):
      """ Writes a header log message.
      
      Args:
         msg (string): The header message.
      """
      self.out.write("########################################################\n")
      self.out.write("~ %s ~\n" % msg)
      self.out.write("########################################################\n")
      
   def getColorEscSeq(self, row, col):  
      
      red = random.randint(0, 255)
      green = random.randint(0, 255)
      blue = random.randint(0, 255)
      
      col_norm = red*red + green*green + blue*blue
      
      # Have black text on dark background color and wi
      if col_norm > 49152:
         forground_color = "0"
      else:
         forground_color = "15"
         
      return "\x1b[48;2;{red};{green};{blue}m" \
             "\x1b[38;5;{forground_color}m" \
         .format(red = red, green = green, blue = blue,
                 forground_color = forground_color)

   def generateKeyString(self, row, col):
      
      layer = _kaleidoscope.Layer.lookupActiveLayer(row, col)
      key = _kaleidoscope.Layer.lookupOnActiveLayer(row, col)
      
      verboseDescription = True
      if key.getFlags() == KEY_FLAGS():
         
         # Normal key
         #
         # TODO: Map the keycode to a (unicode) string that matches the key
         # 
         keyCode = key.getKeyCode()
         if keyCode in hidCodeToString.keys():
            keyString = hidCodeToString[keyCode]
            verboseDescription = False
      
      if verboseDescription:
         keyString = _kaleidoscope.getKeyDescription(layer, row, col)
      
      #if len(keyString) < 4: 
         #return keyString
      
      #return keyString[:4]
      
      colString = self.getColorEscSeq(row, col)
      
      # Limit the key caption to the with of the cell
      #
      #actual_keystring = '{:4.4}'.format(keyString)
      
      return (colString, keyString)
      
      #return '{0}{1}{2}'.format(col_string, actual_keystring, neutral_string)
      
   def graphicalMap(self):
      
      rows = _kaleidoscope.matrixRows()
      cols = _kaleidoscope.matrixCols()
      
      keyStrings = []
      
      
      # Escape sequences to restore default foreground and 
      # background colors
      #
      neutralString = "\x1b[39;49m"  
      
      keyStringMap = {}
      keyStringIndex = 1
      
      for row in range(rows):
         for col in range(cols):
            (colString, keyString) = self.generateKeyString(row, col)
            
            if len(keyString) > 4:
               if not keyString in keyStringMap.keys():
                  keyStringMap[keyString] = keyStringIndex
                  curKeyStringIndex = keyStringIndex
                  keyStringIndex += 1
               else:
                  curKeyStringIndex = keyStringMap[keyString]
                  
               keyString = "*%3.3d" % curKeyStringIndex
            else:
               keyString = '{:4.4}'.format(keyString)
               
            keyStrings.append("{0}{1}{2}".format(
               colString, keyString, neutralString))
      
      #left_upper = '\x250F'.decode("latin-1")   # ┏
      #upper = '\x2501'.decode("latin-1")        # ━
      #right_upper = '\x2513'.decode("latin-1")  # ┓
      #right = '\x2503'.decode("latin-1")        # ┃
      #right_bottom = '\x251b'.decode("latin-1") # ┛
      #bottom = '\x2501'.decode("latin-1")       # ━
      #left_bottom = '\x2517'.decode("latin-1")  # ┗
      #left = '\x2503'.decode("latin-1")         # ┃
      
      #left_gate = '\x2523'.decode("latin-1")    # ┣
      #top_gate = '\x2533'.decode("latin-1")     # ┳
      #right_gate = '\x252b'.decode("latin-1")   # ┫
      #bottom_gate = '\x253b'.decode("latin-1")  # ┻
      
      #cross = '\x254b'.decode("latin-1")        # ╋
      
      #keylist = ...
      
      self.printKeyboardioM01Keymap(keyStrings)
      
      # Print the mapped key strings
      #
      #sortedkeyStringMap = sorted(keyStringMap.items(), key=operator.itemgetter(1))

      for keyString in sorted(keyStringMap, key=keyStringMap.get):
      #print w, d[w]
      #for keyString, keyStringId in sortedkeyStringMap.iteritems():
         self.out.write("%3.3d %s\n" % (keyStringMap[keyString], keyString))
      
   def printKeyboardioM01Keymap(self, keyStrings):
      
      (r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6, r0c7, r0c8, r0c9, r0c10, r0c11, r0c12, r0c13, r0c14, r0c15, \
       r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c6, r1c7, r1c8, r1c9, r1c10, r1c11, r1c12, r1c13, r1c14, r1c15, \
       r2c0, r2c1, r2c2, r2c3, r2c4, r2c5, r2c6, r2c7, r2c8, r2c9, r2c10, r2c11, r2c12, r2c13, r2c14, r2c15, \
       r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r3c6, r3c7, r3c8, r3c9, r3c10, r3c11, r3c12, r3c13, r3c14, r3c15) = \
      tuple(keyStrings)
      
      self.out.write(u"┏━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓        ┏━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓\n")
      self.out.write(u"┃{0}┃{1}┃{2}┃{3}┃{4}┃{5}┃{6}┃        ┃{7}┃{8}┃{9}┃{10}┃{11}┃{12}┃{13}┃\n".format(r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6,        r0c9,  r0c10, r0c11, r0c12, r0c13, r0c14, r0c15))
      self.out.write(u"┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫    ┃        ┃    ┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫\n")
      self.out.write(u"┃{0}┃{1}┃{2}┃{3}┃{4}┃{5}┣━━━━┫        ┣━━━━┫{6}┃{7}┃{8}┃{9}┃{10}┃{11}┃\n".format(r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c10, r1c11, r1c12, r1c13, r1c14, r1c15))
      self.out.write(u"┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫    ┃        ┃    ┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫\n")
      self.out.write(u"┃{0}┃{1}┃{2}┃{3}┃{4}┃{5}┃{6}┃        ┃{7}┃{8}┃{9}┃{10}┃{11}┃{12}┃{13}┃\n".format(r2c0, r2c1, r2c2, r2c3, r2c4, r2c5, r1c6, r1c9, r2c10, r2c11, r2c12, r2c13, r2c14, r2c15))
      self.out.write(u"┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫        ┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫\n")
      self.out.write(u"┃{0}┃{1}┃{2}┃{3}┃{4}┃{5}┃{6}┃        ┃{7}┃{8}┃{9}┃{10}┃{11}┃{12}┃{13}┃\n".format(r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r2c6,        r2c9,  r3c10, r3c11, r3c12, r3c13, r3c14, r3c15))
      self.out.write(u"┗━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━━━━┛        ┗━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━━━━┛\n")
      self.out.write(u"                ┏━━━━┓                                    ┏━━━━┓                \n")
      self.out.write(u"                ┃{0}┣━━━━┓                          ┏━━━━┫{1}┃                \n".format(r0c7, r0c8))
      self.out.write(u"                ┗━━━━┫{0}┣━━━━┓                ┏━━━━┫{1}┣━━━━┛                \n".format(r1c7, r1c8))
      self.out.write(u"                     ┗━━━━┫{0}┣━━━━┓      ┏━━━━┫{1}┣━━━━┛                     \n".format(r2c7, r2c8))
      self.out.write(u"                          ┗━━━━┫{0}┃      ┃{1}┣━━━━┛                          \n".format(r3c7, r3c8))
      self.out.write(u"                               ┗━━━━┛      ┗━━━━┛                               \n")
      self.out.write(u"                    ┏━━━━━━┓                        ┏━━━━━━┓                    \n")
      self.out.write(u"                    ┃ {0} ┃                        ┃ {1} ┃                    \n".format(r3c6, r3c9))
      self.out.write(u"                    ┗━━━━━━┛                        ┗━━━━━━┛                    \n")

##define KEYMAP(                                                                                     \
  #r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6,        r0c9,  r0c10, r0c11, r0c12, r0c13, r0c14, r0c15, \
  #r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c6,        r1c9,  r1c10, r1c11, r1c12, r1c13, r1c14, r1c15, \
  #r2c0, r2c1, r2c2, r2c3, r2c4, r2c5,                     r2c10, r2c11, r2c12, r2c13, r2c14, r2c15, \
  #r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r2c6,        r2c9,  r3c10, r3c11, r3c12, r3c13, r3c14, r3c15, \
              #r0c7, r1c7, r2c7, r3c7,                             r3c8,  r2c8,  r1c8, r0c8,         \
                          #r3c6,                                          r3c9)                      \
  #{                                                                                                 \
    #{r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6, r0c7, r0c8, r0c9, r0c10, r0c11, r0c12, r0c13, r0c14, r0c15}, \
    #{r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c6, r1c7, r1c8, r1c9, r1c10, r1c11, r1c12, r1c13, r1c14, r1c15}, \
    #{r2c0, r2c1, r2c2, r2c3, r2c4, r2c5, r2c6, r2c7, r2c8, r2c9, r2c10, r2c11, r2c12, r2c13, r2c14, r2c15}, \
    #{r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r3c6, r3c7, r3c8, r3c9, r3c10, r3c11, r3c12, r3c13, r3c14, r3c15}, \
  #}