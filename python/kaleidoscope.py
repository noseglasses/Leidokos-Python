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

# For documentation style see http://www.sphinx-doc.org/en/stable/ext/napoleon.html

nIndentChars = 3
cycleIndent = " "*nIndentChars
keyboardReportIndent = " "*(nIndentChars*2)
assertionGroupIndent = " "*(nIndentChars*3)
assertionIndent = " "*(nIndentChars*4)

#class Key(_kaleidoscope.Key): pass

#class Layer(_kaleidoscope.Layer): pass

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
   
class ReportModifierActive(Assertion):
   """ Asserts that a specific modifier is active in the keyboard report.
   
      Args:
         modifier (int): The modifier tested for being active.
   """
   
   def __init__(self, modifier):
      Assertion.__init__(self)
      self.modifier = modifier
      
   def _description(self):
      return "Modifier %s active" % str(_kaleidoscope.modifierToName(self.modifier))

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
      return "Modifier %s inactive" % str(_kaleidoscope.Modifier.toName(self.modifier))

   def _evalInternal(self, keyReport):
      return not keyReport.isModifierActive(self.modifier)
   
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
      
   def __del__(self):
      
      _kaleidoscope.setKeyboardReportCallback(None)
      
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
      _kaleidoscope.keyDown(row, col)
      
   def keyUp(self, row, col):
      """ Registers a key up event. Make sure that the key was registered
      as active before, using keyDown(...).
      
      Args:
         row (int): The keyboard key row.
         col (int): The keyboard key col.
      """
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
      self.out.write("Single scan cycle\n")
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
      
   def scanCycles(self, n, onStopAssertionList = None):
      """ Executes a number of scan cycles and processes assertions afterwards.
      
      Args:
         n (int): The number of cycles to execute.
         onStopAssertionList (list): A list of assertions to be executed after
            the cycles where executed and to be discarded afterwards. Defaults
            to None.
      """
      
      self.out.write("Running %d cycles\n" % n)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            self._configureTemporaryAssertion(assertion)
            
      for i in range(0, n):
         self._scanCycle()
         
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
            self.assertion._report(self.out)
         elif self.debug:
            self.assertion._report(self.out)
         
         self.assertionsPassed &= assertionPassed
   