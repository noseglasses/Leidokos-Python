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

from _indentation import *

class _Assertion(object):
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

class _AssertionGroup(_Assertion):
   """ Groups several assertions.
   
      Args:
         assertionList (list): A list of assertions.
   """

   def __init__(self, assertionList):
      _Assertion.__init__(self)
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
         
class ReportNthCycle(_Assertion):
   """ Asserts that the current cycle is the nth.
   
      Args:
         cycle (int): The cycle count.
   """
   
   def __init__(self, cycle):
      _Assertion.__init__(self)
      self.cycle = cycle
   
   def _description(self):
      return "Is %d. cycle" % self.cycle

   def _actualState(self):
      return "%d. cycle" % self._getTest().cycleId
   
   def _evalInternal(self, dummy):
      return self._getTest().cycleId == self.cycle