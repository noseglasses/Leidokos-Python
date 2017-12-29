#!/usr/bin/python3

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
import kaleidoscope

from kaleidoscope import *

import sys

test = Test()
test.debug = True

# The assertions are evaluated in the next loop cycle
#
test.queueGroupedReportAssertions([ 
      ReportNthInCycle(1), 
      ReportNthCycle(1),
      ReportKeyActive(keyA()),
      ReportKeyActive(keyB()),
      ReportModifierActive(modSHIFT_HELD()),
      DumpReport()
   ])

test.keyDown(2, 1)

test.scanCycle()

test.keyUp(2, 1)

test.scanCycles(2)

test.skipTime(20)
