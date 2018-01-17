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
from _Assertion import ReportNthCycle

class CycleHasNReports(_Assertion):
   """ Asserts that there was a specific number of keyboard reports generated
      within a cycle.
      
      Args:
         nReports (int): The required number of reports.
   """
   
   def __init__(self, nReports):
      _Assertion.__init__(self)
      self.nReports = nReports
   
   def _description(self):
      return "There were %d keyboard reports in cycle" % self.nReports

   def _actualState(self):
      return "%d keyboard reports" % self._getTestDriver().nReportsInCycle
   
   def _evalInternal(self, dummy):
      return self._getTestDriver().nReportsInCycle == self.nReports
   
class NReportsGenerated(_Assertion):
   """ Asserts that there was a specific number of keyboard reports generated
         since the assertion was instanciated.
         
      Args:
         nReports (int): The required number of reports.
   """
   
   def __init__(self, nReports):
      _Assertion.__init__(self)
      self.nReports = nReports
      
   # Override the _setTest method to enable setting 
   # the startNReports once the reference to the parent
   # test driver is available
   #
   def _setTestDriver(self, testDriver):
      _Assertion._setTestDriver(self, testDriver)
      self.startNReports = self._getTestDriver().nKeyboardReports
   
   def _description(self):
      return "There were %d keyboard reports in cycle" % self.nReports
   
   def _reportsGenerated(self):
      return self._getTestDriver().nKeyboardReports - self.startNReports
   
   def _actualState(self):
      return "%d keyboard reports" % self._reportsGenerated()
   
   def _evalInternal(self, dummy):
      return self._reportsGenerated() == self.nReports
   
class CycleIsNth(ReportNthCycle):
   """ Asserts that the current cycle is the nth.
   
      Args:
         cycle (int): The cycle count.
   """
   pass

class LayerIsActive(_Assertion):
   """ Asserts that a given layer is active (the current top layer).
      
      Args:
         layer (int): The id of the required layer.
   """
   
   def __init__(self, layer):
      _Assertion.__init__(self)
      self.layer = layer
   
   def _description(self):
      return "Is %d. layer active" % self.layer

   def _actualState(self):
      return "%d. layer is active" % kaleidoscope.Layer.top()
   
   def _evalInternal(self, dummy):
      return kaleidoscope.top() == self.layer
   
class LayerIsInactive(_Assertion):
   """ Asserts that a given layer is currently not active (not the current top layer).
      
      Args:
         layer (int): The id of the layer required to be not active.
   """
   
   def __init__(self, layer):
      _Assertion.__init__(self)
      self.layer = layer
   
   def _description(self):
      return "Is %d. layer inactive" % self.layer

   def _actualState(self):
      return "%d. layer is active" % kaleidoscope.Layer.top()
   
   def _evalInternal(self, dummy):
      return kaleidoscope.top() != self.layer
   
class TimeElapsedGreater(_Assertion):
   """ Asserts that that time that elapsed is greater than a given time in [ms].
      
      Args:
         startT (float): The reference start time.
         deltaT (float): The time in [ms] that is required to have elapsed.
   """
   
   def __init__(self, startT, deltaT):
      _Assertion.__init__(self)
      self.startT = startT
      self.deltaT  = deltaT 
   
   def _description(self):
      return "Time elapsed greater %f ms" % self.layer

   def _actualState(self):
      return "Time elapsed is %f ms" % (test.time - self.startT)
   
   def _evalInternal(self, dummy):
      return test.time - self.startT > self.deltaT