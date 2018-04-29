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

import weakref
import sys
import os
import importlib

import kaleidoscope
from kaleidoscope import *
from _indentation import *

def _removeItemsFromList(fromList, removalList):
   """ Removes all items from a list.
   
   Args:
      fromList (list): The list to remove entries from.
      removalList (list): The list that contains the entries to remove.
      
   Returns:
      list: Copy of fromList with items removed.
   """
   return [assertion for assertion in fromList if assertion not in removalList]

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
      
class TestDriver(object):
   """ The main test object that controls everything.
   
   Attributes:
      out (stream): A stream that should be used for all output using write(...).
      
      debug (bool): Additional output is generated when set to True. Defaults to False.
   """
   def __init__(self, 
                out = sys.stdout, 
                debug = False, 
                cycleDuration = 5,
                noExit = False):
      
      self.assertionsPassed = True
      self.nReportsInCycle = 0
      self.nKeyboardReports = 0
      
      # The cycle duration in ms
      #
      self.cycleDuration = cycleDuration
      self.cycleId = 0
      self.time = 0
      
      self.scanCyclesDefaultCount = 5
      
      # The preferred output
      #
      self.out = _TimedStream(self, out)
      
      self.queuedReportAssertions = []
      self.permanentReportAssertions = []
      self.queuedCycleAssertions = []
      self.permanentCycleAssertions = []
      
      # Enable the following flag if you want strict errors to be 
      # triggered whenever there are keyboard reports for which no
      # assertions have been specified.
      #
      self.errorIfReportWithoutQueuedAssertions = False
      
      self.debug = debug
      
      kaleidoscope.setKeyboardReportCallback(_KeyboardReportCallbackProxy(self))
   
      kaleidoscope.init()
      
      self.initHardware()
      
      self._headerText()
      
      self.noExit = noExit
      #try:
         #__NO_EXIT__
      #except NameError:
         #self.noExit = True
      #else:
         #self.noExit = False
      
   def __del__(self):
      
      kaleidoscope.finalize()
      
      self._footerText()
      
      if not self.checkStatus():
         if not self.noExit:
            self._error("Terminating with exit code 1")
         
   def setOutputStream(self, out):
      """ Sets an output stream that is used for all formatted output.
      
      Args:
         out (stream): An output stream.
      """
      self.out = _TimedStream(self, out)
      
   def initHardware(self):
      
      #hardwareIDString = kaleidoscope.getHardwareIDString()
      hardwareModuleName = ("Hardware-Model01")
      
      hardwareModule = importlib.import_module(hardwareModuleName)
      
      self.hardware = hardwareModule.Hardware()
         
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
      self.out.writeN("Leidokos-Python\n")
      self.out.writeN("\n")
      self.out.writeN("author: noseglasses (https://github.com/noseglasses, shinynoseglasses@gmail.com)\n")
      self.out.writeN("version: %s\n" % kaleidoscope.getVersionString())
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
      
   def checkStatus(self):
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
      else:
         self._error("Errors occurred\n")
      
      return False

   def _configureReportAssertions(self, assertionList):
      for assertion in assertionList:
         self._configureReportAssertion(assertion)
         
   def _configureReportAssertion(self, assertion):
      assertion._setTestDriver(self)
      assertion.typeKeyword = "Report"
      
   def queueReportAssertion(self, assertion):
      """ Queues a report assertions. The report assertion at the end of 
      the queue will be cast on the next key report. Then the respective 
      assertion will be discarded.
      
      Args:
         assertion (_Assertion): The assertion to add to the queue.
      """
      self._configureReportAssertion(assertion)
      self.queuedReportAssertions.append(assertion)
      
   def _generateAssertionGroup(self, assertionList):
      for assertion in assertionList:
         self._configureReportAssertion(assertion)
         
      from _Assertion import _AssertionGroup
      assertionGroup = _AssertionGroup(assertionList)
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
         assertion (_Assertion): An assertions to be used permanently.
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
      
      self.out.write("Processing keyboard report %d (%d. in cycle %d)\n"
                     % (self.nKeyboardReports,
                        self.nReportsInCycle,
                        self.cycleId), keyboardReportIndent)
                     
      nAssertionsQueued = len(self.queuedReportAssertions)
      
      self.out.write("%d queued report assertions\n" % len(self.queuedReportAssertions), assertionGroupIndent)
      
      if len(self.queuedReportAssertions) > 0:
         self._processReportAssertion(self.queuedReportAssertions[0], keyReport)
         self.queuedReportAssertions.pop(0)
         
      if len(self.permanentReportAssertions) > 0:
         
         self.out.write("%d permanent report assertions\n" % len(self.permanentReportAssertions), assertionGroupIndent)
         for assertion in self.permanentReportAssertions:
            self._processReportAssertion(assertion, keyReport)
            
      if (nAssertionsQueued == 0) and self.errorIfReportWithoutQueuedAssertions:
         self._error("Encountered a report without assertions being queued")
         
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
      
      kaleidoscope.keyDown(row, col)
      
   def keyUp(self, row, col):
      """ Registers a key up event. Make sure that the key was registered
      as active before, using keyDown(...).
      
      Args:
         row (int): The keyboard key row.
         col (int): The keyboard key col.
      """
      self.out.write("- Releasing key (%d, %d)\n" % (row, col))
      kaleidoscope.keyUp(row, col)
      
   def isKeyPressed(self, row, col):
      return kaleidoscope.isKeyPressed(row, col)
   
   def tap(self, row, col):
      """ Registers tap of a key.
      
      Args:
         row (int): The keyboard key row.
         col (int): The keyboard key col.
      """
      kaleidoscope.tap(row, col)

   def clearAllKeys(self):
      """ Clears all keys that are currently active (down). """
      self.out.write("- Clearing all keys\n")
      kaleidoscope.clearAllKeys()
      
   def _configureCycleAssertion(self, assertion):
      assertion._setTestDriver(self)
      assertion.typeKeyword = "Cycle"
      
   def _configureTemporaryAssertion(self, assertion):
      assertion._setTestDriver(self)
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
      
   def _scanCycle(self, onStopAssertionList = None, onlyLogReports = False):
      
      self.cycleId += 1
      self.nReportsInCycle = 0
      
      if not onlyLogReports:
         self.out.write("Scan cycle %d\n" % self.cycleId, cycleIndent)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            self._configureTemporaryAssertion(assertion)
      
      kaleidoscope.scanCycle()
      
      if self.nReportsInCycle == 0:
         if not onlyLogReports:
            self.out.write("No keyboard reports processed\n", keyboardReportIndent)
      else:
         self.out.write("%d keyboard reports processed\n" % self.nReportsInCycle, keyboardReportIndent)
      
      self.time += self.cycleDuration
      
      kaleidoscope.setMillis(self.time)
      
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
      
   def scanCycles(self, n = 0, onStopAssertionList = None, cycleAssertionList = None):
      """ Executes a number of scan cycles and processes assertions afterwards.
      
      Args:
         n (int): The number of cycles to execute.
         onStopAssertionList (list): A list of assertions to be executed after
            the cycles where executed and to be discarded afterwards. Defaults
            to None.
         cycleAssertionList (list): A list of assertions that are executed
            after every cycle.
      """
      
      if n == 0:
         n = self.scanCyclesDefaultCount
      
      self.out.write("Running %d scan cycles\n" % n)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            self._configureTemporaryAssertion(assertion)
            
      for i in range(0, n):
         self._scanCycle(cycleAssertionList, onlyLogReports = True)
         
      if onStopAssertionList and len(onStopAssertionList) > 0:
         self.out.write("Processing %d cycle assertions on stop\n" % len(onStopAssertionList), cycleIndent)
         self._processCycleAssertions(onStopAssertionList)
         
      self.out.write("\n")
         
   def skipTime(self, deltaT , onStopAssertionList = None):
      """ Skips a given amount of time by executing cycles and processes assertions afterwards.
      
      Important:
         Make sure to set the cycleDuration property of the TestDriver class 
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
            self._configureTemporaryAssertion(assertion)
            
      startTime = self.time
      
      elapsedTime = 0
      while elapsedTime < deltaT:
         self._scanCycle(onlyLogReports = True)
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
         
         #assertion._setTestDriver(self)
         
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
      
   def rawLog(self, msg):
      """ Writes a log message without time information.
      
      Args:
         msg (string): The log message.
      """
      self.out.write("%s\n" % msg, outputTime = False)
      
   def description(self, msg):
      """ Writes a description message without time information.
      
      Args:
         msg (string): The description message.
      """
      self.out.write("%s" % msg, outputTime = False)
   
   def header(self, msg):
      """ Writes a header log message.
      
      Args:
         msg (string): The header message.
      """
      self.out.write("########################################################\n")
      self.out.write("%s\n" % msg)
      self.out.write("########################################################\n")
      
   def graphicalMap(self):
      import GraphicalMap
      GraphicalMap.graphicalMap(self.out, self.hardware)
      
   def _initKeyboard(self):
      """ Resets the keyboard to initial state.
      """
      kaleidoscope.clearAllKeys()
      hid.initializeKeyboard()
      
   def runTest(self, methodName):
      
      assert len(self.queuedReportAssertions) == 0
      assert len(self.queuedCycleAssertions) == 0
      
      self._initKeyboard()
      getattr(self, methodName)()
      
