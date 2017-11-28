# -*- mode: c++ -*-
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
#
import kaleidoscope
import sys
import weakref
import os

class KeyboardReportAssertion(object):
   
   def __init__(self, key):
      pass
      
   def evalInternal(self, keyReport):
      return True
      
   def eval(self, keyReport):
      
      sys.stdout.write("%s.eval()\n" % self.__class__.__name__)
      
      if not self.evalInternal(keyReport):
         self.valid = False
         return False
      
      self.valid = True
      return True
   
   def report(self, out):
      if self.valid:
         out.write("Assertion passed: %s\n" % self.description())
      else:
         out.write("Assertion failed: %s\n" % self.description())
         theActualState = self.actualState()
         if theActualState:
            out.write("   actual: %s\n" % theActualState)
   
   def actualState(self):
      return None

   def setTest(self, test):
      self.test = test

class KeyActive(KeyboardReportAssertion):
   
   def __init__(self, key):
      self.key = key
      
   def description(self):
      return "Key %s active" % str(kaleidoscope.Key.keyToName(self.key))

   def evalInternal(self, keyReport):
      return keyReport.isKeyActive(self.key)
   
class KeyInactive(KeyboardReportAssertion):
   
   def __init__(self, key):
      self.key = key
      
   def description(self):
      return "Key %s inactive" % str(kaleidoscope.Key.keyToName(self.key))

   def evalInternal(self, keyReport):
      return not keyReport.isKeyActive(self.key)
   
class KeycodeActive(KeyboardReportAssertion):
   
   def __init__(self, keycode):
      self.keycode = keycode
      
   def description(self):
      return "Keycode %s active" % str(kaleidoscope.Key.keycodeToName(self.keycode))

   def evalInternal(self, keyReport):
      return keyReport.isKeycodeActive(self.keycode)
   
class KeycodeInactive(KeyboardReportAssertion):
   
   def __init__(self, keycode):
      self.keycode = keycode
      
   def description(self):
      return "Keycode %s inactive" % str(kaleidoscope.Key.keycodeToName(self.keycode))

   def evalInternal(self, keyReport):
      return not keyReport.isKeycodeActive(self.keycode)
   
class ModifierActive(KeyboardReportAssertion):
   
   def __init__(self, modifier):
      self.modifier = modifier
      
   def description(self):
      return "Modifier %s active" % str(kaleidoscope.Modifier.toName(self.modifier))

   def evalInternal(self, keyReport):
      return keyReport.isModifierActive(self.modifier)
   
class ModifierInactive(KeyboardReportAssertion):
   
   def __init__(self, modifier):
      self.modifier = modifier
      
   def description(self):
      return "Modifier %s inactive" % str(kaleidoscope.Modifier.toName(self.modifier))

   def evalInternal(self, keyReport):
      return not keyReport.isModifierActive(self.modifier)
   
class NthReportInCycle(KeyboardReportAssertion):
   
   def __init__(self, n):
      self.n = n
   
   def description(self):
      return "Is %d. report in cycle" % self.n

   def evalInternal(self, keyReport):
      return self.test.nReportsInCycle == self.n
   
   def actualState(self):
      return "%d. report in cycle" % self.test.nReportsInCycle
   
class NthCycle(KeyboardReportAssertion):
   
   def __init__(self, cycle):
      self.cycle = cycle
   
   def description(self):
      return "Is %d. cycle" % self.cycle

   def actualState(self):
      return "%d. cycle" % kaleidoscope.currentCycle()
   
   def evalInternal(self, keyReport):
      return kaleidoscope.currentCycle() == self.cycle
   
class AssertionGroup(KeyboardReportAssertion):
   
   def __init__(self, assertionList):
      self.assertionList = assertionList
   
   def report(self, out):
      for assertion in self.assertionList:
         assertion.report(out) 

   def evalInternal(self, keyReport):
      
      sys.stdout.write("%s.evalInternal()\n" % self.__class__.__name__)
      
      self.valid = True
      for assertion in self.assertionList:
         self.valid |= assertion.eval(keyReport)
         
      return self.valid
   
   def setTest(self, test):
      for assertion in self.assertionList:
         assertion.setTest(test)
   
class KeyboardReportCallbackProxy(object):
   
   def __init__(self, test):
      self.test = weakref.ref(test)
   
   def processReport(self, keyboardReport):
      self.test().processReport(keyboardReport)
   
class Test(object):
   
   def __init__(self):
      
      self.assertionQueue = []
      self.assertionsPassed = True
      self.lastReportInCycle = kaleidoscope.currentCycle()
      self.nReportsInCycle = 0
      self.nKeyboardReports = 0
      
      self.debug = False
      
      kaleidoscope.setKeyboardReportCallback(KeyboardReportCallbackProxy(self))
      
      kaleidoscope.init()
      
   def __del__(self):
      
      kaleidoscope.setKeyboardReportCallback(None)
      
      self.checkAssertions()
      
   def checkAssertions(self):
      success = True
      if len(self.assertionQueue) > 0:
         sys.stdout.write("Error: There are %d leftover assertions in the queue\n" % len(self.assertionQueue))
         success = False
      
      if not self.assertionsPassed:
         sys.stdout.write("Error: Not all assertions passed\n")
         success = False
         
      if success:
         sys.stdout.write("All tests passed.\n")
      else:
         os._exit(1)

   def addAssertion(self, assertion):
      assertion.setTest(self)
      self.assertionQueue.append(assertion)
      
   def addAssertions(self, assertionList):
      assertionGroup = AssertionGroup(assertionList)
      assertionGroup.setTest(self)
      self.assertionQueue.append(assertionGroup)
      
   def processReport(self, keyReport):
      
      sys.stdout.write("Processing report\n")
      
      self.nKeyboardReports += 1
      
      if kaleidoscope.currentCycle() > self.lastReportInCycle:
         self.nReportsInCycle = 0
         self.lastReportInCycle = kaleidoscope.currentCycle()
         
      self.nReportsInCycle += 1
      
      sys.stdout.write("%d assertions in the queue\n" % len(self.assertionQueue))
      
      if len(self.assertionQueue) > 0:
         assertionPassed = self.assertionQueue[0].eval(keyReport)
         
         if not assertionPassed:
            self.assertionQueue[0].report(sys.stdout)
         elif self.debug:
            self.assertionQueue[0].report(sys.stdout)
         
         self.assertionsPassed |= assertionPassed
         
         self.assertionQueue.pop(0)