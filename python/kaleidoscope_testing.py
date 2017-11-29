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
   
def removeItemsFromList(fromList, removalList):
   return [assertion for assertion in fromList if assertion not in removalList]

class Assertion(object):
   
   def __init__(self):
      self.typeKeyword = ""
   
   def report(self, out):
      if self.valid:
         out.write("%s assertion passed: %s\n" % (self.typeKeyword, self.description()))
      else:
         out.write("*** %s assertion failed: %s\n" % (self.typeKeyword, self.description()))
         theActualState = self.actualState()
         if theActualState:
            out.write("   actual: %s\n" % theActualState)
        
   def evalInternal(self, target):
      return True
      
   def eval(self, target):
      
      #sys.stdout.write("%s.eval()\n" % self.__class__.__name__)
      
      if not self.evalInternal(target):
         self.valid = False
         return False
      
      self.valid = True
      return True
   
   def actualState(self):
      return None

   def setTest(self, test):
      self.testWeak = weakref.ref(test)
      
   def getTest(self):
      return self.testWeak()
   
class AssertionGroup(Assertion):
   
   def __init__(self, assertionList):
      Assertion.__init__(self)
      self.assertionList = assertionList
   
   def report(self, out):
      for assertion in self.assertionList:
         assertion.report(out) 

   def evalInternal(self, keyReport):
      
      #sys.stdout.write("%s.evalInternal()\n" % self.__class__.__name__)
      
      self.valid = True
      for assertion in self.assertionList:
         self.valid &= assertion.eval(keyReport)
         
      return self.valid
   
   def setTest(self, test):
      for assertion in self.assertionList:
         assertion.setTest(test)

################################################################################
# Key report assertions
################################################################################

class ReportKeyActive(Assertion):
   
   def __init__(self, key):
      Assertion.__init__(self)
      self.key = key
      
   def description(self):
      return "Key %s active" % str(kaleidoscope.Key.keyToName(self.key))

   def evalInternal(self, keyReport):
      return keyReport.isKeyActive(self.key)
   
class ReportKeyInactive(Assertion):
   
   def __init__(self, key):
      Assertion.__init__(self)
      self.key = key
      
   def description(self):
      return "Key %s inactive" % str(kaleidoscope.Key.keyToName(self.key))

   def evalInternal(self, keyReport):
      return not keyReport.isKeyActive(self.key)
   
class ReportKeycodeActive(Assertion):
   
   def __init__(self, keycode):
      Assertion.__init__(self)
      self.keycode = keycode
      
   def description(self):
      return "Keycode %s active" % str(kaleidoscope.Key.keycodeToName(self.keycode))

   def evalInternal(self, keyReport):
      return keyReport.isKeycodeActive(self.keycode)
   
class ReportKeycodeInactive(Assertion):
   
   def __init__(self, keycode):
      Assertion.__init__(self)
      self.keycode = keycode
      
   def description(self):
      return "Keycode %s inactive" % str(kaleidoscope.Key.keycodeToName(self.keycode))

   def evalInternal(self, keyReport):
      return not keyReport.isKeycodeActive(self.keycode)
   
class ReportModifierActive(Assertion):
   
   def __init__(self, modifier):
      Assertion.__init__(self)
      self.modifier = modifier
      
   def description(self):
      return "Modifier %s active" % str(kaleidoscope.Modifier.toName(self.modifier))

   def evalInternal(self, keyReport):
      return keyReport.isModifierActive(self.modifier)
   
class ReportModifierInactive(Assertion):
   
   def __init__(self, modifier):
      Assertion.__init__(self)
      self.modifier = modifier
      
   def description(self):
      return "Modifier %s inactive" % str(kaleidoscope.Modifier.toName(self.modifier))

   def evalInternal(self, keyReport):
      return not keyReport.isModifierActive(self.modifier)
   
class ReportNthInCycle(Assertion):
   
   def __init__(self, n):
      Assertion.__init__(self)
      self.n = n
   
   def description(self):
      return "Is %d. report in cycle" % self.n

   def evalInternal(self, keyReport):
      return self.getTest().nReportsInCycle == self.n
   
   def actualState(self):
      return "%d. report in cycle" % self.getTest().nReportsInCycle
   
class ReportNthCycle(Assertion):
   
   def __init__(self, cycle):
      Assertion.__init__(self)
      self.cycle = cycle
   
   def description(self):
      return "Is %d. cycle" % self.cycle

   def actualState(self):
      return "%d. cycle" % self.getTest().cycleId
   
   def evalInternal(self, keyReport):
      return self.getTest().cycleId == self.cycle
   
class DumpReport(Assertion):
   
   def evalInternal(self, keyReport):
      self.keyReport = keyReport
      return True
   
   def description(self):
      return "Dump report: %s" % self.keyReport.dump()
         
################################################################################
# General assertions
################################################################################

class CycleHasNReports(Assertion):
   
   def __init__(self, nReports):
      Assertion.__init__(self)
      self.nReports = nReports
   
   def description(self):
      return "There were %d. keyboard reports in cycle" % self.nReports

   def actualState(self):
      return "%d. keyboard reports" % self.getTest().nReportsInCycle
   
   def evalInternal(self, dummy):
      return self.getTest().nReportsInCycle == self.nReports
   
class CycleIsNth(Assertion):
   
   def __init__(self, n):
      Assertion.__init__(self)
      self.n = n
   
   def description(self):
      return "Is %d. cycle" % self.n

   def actualState(self):
      return "%d. cycle" % test.cycleId
   
   def evalInternal(self, dummy):
      return test.cycleId == self.n

class LayerIsActive(Assertion):
   
   def __init__(self, layer):
      Assertion.__init__(self)
      self.layer = layer
   
   def description(self):
      return "Is %d. layer active" % self.layer

   def actualState(self):
      return "%d. layer is active" % kaleidoscope.Layer.top()
   
   def evalInternal(self, dummy):
      return kaleidoscope.top() == self.layer
   
class LayerIsInactive(Assertion):
   
   def __init__(self, layer):
      Assertion.__init__(self)
      self.layer = layer
   
   def description(self):
      return "Is %d. layer inactive" % self.layer

   def actualState(self):
      return "%d. layer is active" % kaleidoscope.Layer.top()
   
   def evalInternal(self, dummy):
      return kaleidoscope.top() != self.layer
   
class TimeElapsedGreater(Assertion):
   
   def __init__(self, startT, deltaT ):
      Assertion.__init__(self)
      self.startT = startT
      self.deltaT  = deltaT 
   
   def description(self):
      return "Time elapsed greater %f ms" % self.layer

   def actualState(self):
      return "Time elapsed is %f ms" % (test.time - self.startT)
   
   def evalInternal(self, dummy):
      return test.time - self.startT > self.deltaT
   
################################################################################
# Main test class
################################################################################
   
class KeyboardReportCallbackProxy(object):
   
   def __init__(self, test):
      self.testWeak = weakref.ref(test)
   
   def processReport(self, keyboardReport):
      self.testWeak().processReport(keyboardReport)
   
class Test(object):
   
   def __init__(self):
      
      self.assertionsPassed = True
      self.nReportsInCycle = 0
      self.nKeyboardReports = 0
      
      # The cycle duration in ms
      #
      self.cycleDuration = 0
      self.cycleId = 0
      self.time = 0
      
      # The preferred output
      #
      self.out = sys.stdout
      
      self.queuedReportAssertions = []
      self.permanentReportAssertions = []
      self.queuedCycleAssertions = []
      self.permanentCycleAssertions = []
      
      self.debug = False
      
      kaleidoscope.setKeyboardReportCallback(KeyboardReportCallbackProxy(self))
      
      kaleidoscope.init()
      
      self.headerText()
      
   def __del__(self):
      
      kaleidoscope.setKeyboardReportCallback(None)
      
      self.footerText()
      
      if not self.checkStatus():
         self.error("Terminating with exit code 1")
         
   def error(self, msg):
      self.out.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
      self.out.write("*** Error: %s\n" % msg)
      self.out.write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        
      os._exit(1)
      
   def headerText(self):
      self.out.write("################################################################################\n")
      self.out.write("Starting Kaleidoscope keyboard firmware testing\n")
      self.out.write("################################################################################\n")
      
   def footerText(self):
      self.out.write("################################################################################\n")
      self.out.write("Kaleidoscope keyboard firmware testing done\n")
      self.out.write("################################################################################\n")
      
   def checkStatus(self):
      success = True
      if len(self.queuedReportAssertions) > 0:
         self.out.write("*** Error: There are %d left over assertions in the queue\n" % len(self.queuedReportAssertions))
         success = False
      
      if not self.assertionsPassed:
         self.out.write("*** Error: Not all assertions passed\n")
         success = False
         
      if success:
         self.out.write("All tests passed.\n")
         return True
      
      return False

   def configureReportAssertions(self, assertionList):
      for assertion in assertionList:
         self.configureReportAssertion(assertion)
         
   def configureReportAssertion(self, assertion):
      assertion.setTest(self)
      assertion.typeKeyword = "Report"
      
   def queueReportAssertion(self, assertion):
      self.configureReportAssertion(assertion)
      self.queuedReportAssertions.append(assertion)
      
   def generateAssertionGroup(self, assertionList):
      for assertion in assertionList:
         self.configureReportAssertion(assertion)
      assertionGroup = AssertionGroup(assertionList)
      self.configureReportAssertion(assertionGroup)
      return assertionGroup
      
   def queueReportAssertions(self, assertionList):
      self.queuedReportAssertions.append(
         self.generateAssertionGroup(assertionList))
      
   def removeQueuedReportAssertions(self, assertionList):
      self.queuedReportAssertions = \
         removeItemsFromList(self.queuedReportAssertions, assertionList)
      
   def addPermanentReportAssertion(self, assertion):
      self.configureReportAssertion(assertion)
      self.permanentReportAssertions.append(assertion)
      
   def addPermanentReportAssertions(self, assertionList):
      self.configureReportAssertions(assertionList)
      self.permanentReportAssertions.extend(assertionList)
      
   def removePermanentReportAssertions(self, assertionList):
      self.permanentReportAssertions = \
         removeItemsFromList(self.permanentReportAssertions, assertionList)
      
   def removeReportAssertions(self, assertionList):
      self.removeQueuedReportAssertions(assertionList)
      self.removePermanentReportAssertions(assertionList)
      
   def processReport(self, keyReport):
      
      self.nKeyboardReports += 1
         
      self.nReportsInCycle += 1
      
      self.out.write("Processing %d. keyboard report (%d. in cycle)\n"
                     % (self.nKeyboardReports, self.nReportsInCycle))
      
      self.out.write("%d report assertions in queue\n" % len(self.queuedReportAssertions))
      
      if len(self.queuedReportAssertions) > 0:
         self.processReportAssertion(self.queuedReportAssertions[0], keyReport)
         self.queuedReportAssertions.pop(0)
         
      if len(self.permanentReportAssertions) > 0:
         
         self.out.write("%d permanent report assertions\n" % len(self.permanentReportAssertions))
         for assertion in self.permanentReportAssertions:
            self.processReportAssertion(assertion, keyReport)
         
   def processReportAssertion(self, assertion, keyReport):
      
      assertionPassed = assertion.eval(keyReport)
      
      if not assertionPassed or self.debug:
         assertion.report(self.out)
      
      self.assertionsPassed &= assertionPassed
         
   # Some wrapper functions for kaleidoscope stuff
   
   def keyDown(self, row, col):
      kaleidoscope.keyDown(row, col)
      
   def keyUp(self, row, col):
      kaleidoscope.keyUp(row, col)
   
   def tap(self, row, col):
      kaleidoscope.tap(row, col)
      
   def clearAllKeys(self):
      kaleidoscope.clearAllKeys()
      
   def configureCycleAssertion(self, assertion):
      assertion.setTest(self)
      assertion.typeKeyword = "Cycle"
      
   def configureTemporaryAssertion(self, assertion):
      assertion.setTest(self)
      assertion.typeKeyword = "Temporary cycle"
      
   def queueCycleAssertions(self, assertionList):
      for assertion in assertionList:
         self.configureReportAssertion(assertion)
      
      self.queuedCycleAssertions.extend(assertionList)
      
   def removeQueuedCycleAssertions(self, assertionList):
      self.queuedCycleAssertions = \
         removeItemsFromList(self.queuedCycleAssertions, assertionList)
      
   def registerPermanentCycleAssertions(self, assertionList):
      for assertion in assertionList:
         self.configureReportAssertion(assertion)
      
      self.permanentCycleAssertions.extend(assertionList)
      
   def removePermanentCycleAssertions(self, assertionList):
      self.queuedCycleAssertions = \
         removeItemsFromList(self.permanentCycleAssertions, assertionList)
      
   def removeCycleAssertions(self, assertionList):
      self.removeQueuedCycleAssertions(assertionList)
      self.removePermanentCycleAssertions(assertionList)
      
   def loopCycle(self, onStopAssertionList = None):
      
      self.cycleId += 1
      self.nReportsInCycle = 0
      
      self.out.write("Loop cycle %d\n" % self.cycleId)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            self.configureTemporaryAssertion(assertion)
      
      kaleidoscope.loop()
      
      if self.nReportsInCycle == 0:
         self.out.write("   no keyboard reports\n")
      else:
         self.out.write("   %d keyboard reports\n" % self.nReportsInCycle)
      
      self.time += self.cycleDuration
      
      if onStopAssertionList and len(onStopAssertionList) > 0:
         self.out.write("Processing %d cycle assertions on stop\n" % len(onStopAssertionList))
         self.processCycleAssertions(onStopAssertionList)
      
      if len(self.queuedCycleAssertions) > 0:
         self.out.write("Processing %d queued cycle assertions\n" % len(self.queuedCycleAssertions))
         self.processCycleAssertions(self.queuedCycleAssertions)
         
         self.queuedCycleAssertions = []
      
      if len(self.permanentCycleAssertions) > 0:
         self.out.write("Processing %d permanent cycle assertions\n" % len(self.permanentCycleAssertions))
         self.processCycleAssertions(self.permanentCycleAssertions)
      
   def loopCycles(self, n, onStopAssertionList = None):
      
      self.out.write("Running %d cycles\n" % n)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            self.configureTemporaryAssertion(assertion)
            
      for i in range(0, n):
         self.loopCycle()
         
      if onStopAssertionList and len(onStopAssertionList) > 0:
         self.out.write("Processing %d cycle assertions on stop\n" % len(onStopAssertionList))
         self.processCycleAssertions(onStopAssertionList)
         
   def skipTime(self, deltaT , onStopAssertionList = None):
      
      self.checkCycleDurationSet()
      
      self.out.write("Skipping dt >= %f ms\n" % deltaT)
      
      if onStopAssertionList:
         for assertion in onStopAssertionList:
            assertion.setTest(self)
            
      startTime = self.time
      
      elapsedTime = 0
      while elapsedTime < deltaT:
         self.loopCycle()
         elapsedTime = self.time - startTime
         
      self.out.write("%f ms skipped\n" % elapsedTime)
         
      if onStopAssertionList and len(onStopAssertionList) > 0:
         self.out.write("Processing %d cycle assertions on stop\n" % len(onStopAssertionList))
         self.processCycleAssertions(onStopAssertionList)
         
   def checkCycleDurationSet(self):
      if self.cycleDuration == 0:
         self.error("Please set test.cycleDuration to a value in "
            "[ms] greater zero before using time based testing")
         
   def processCycleAssertions(self, assertionList):
      
      if not assertionList:
         return
      
      if len(assertionList) == 0:
         return
      
      for assertion in assertionList:
         
         assertion.setTest(self)
         
         assertionPassed = assertion.eval(self)
         
         if not assertionPassed:
            self.assertion.report(self.out)
         elif self.debug:
            self.assertion.report(self.out)
         
         self.assertionsPassed &= assertionPassed
   