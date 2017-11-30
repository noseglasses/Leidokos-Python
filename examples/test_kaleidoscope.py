#!/usr/bin/python

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
import kaleidoscope_testing

from kaleidoscope_testing import *

import sys

test = Test()
test.debug = True

test.keyDown(2, 1)

assertions = [ 
      ReportNthInCycle(1), 
      ReportNthCycle(1),
      ReportKeyActive(kaleidoscope.Key.A()),
      ReportKeyActive(kaleidoscope.Key.B()),
      ReportModifierActive(kaleidoscope.Key.SHIFT_HELD()),
      DumpReport()
   ]

n = 3
someAssertions = assertions[0:3]

# The assertions are evaluated in the next loop cycle
#
test.addPermanentReportAssertions(assertions)

test.loopCycle()

test.keyUp(2, 1)

test.loopCycles(2)

test.skipTime(200)

test.removeReportAssertions(someAssertions)