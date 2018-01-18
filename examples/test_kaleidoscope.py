#!/usr/bin/python3

# -*- mode: c++ -*-
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
import leidokos
from leidokos import *

import sys

driver = TestDriver()
driver.debug = True

# The assertions are evaluated in the next loop cycle
#
driver.queueGroupedReportAssertions([ 
      ReportNthInCycle(1), 
      ReportNthCycle(1),
      ReportKeyActive(keyA()),
      ReportKeyActive(keyB()),
      ReportModifierActive(modSHIFT_HELD()),
      DumpReport()
   ])

driver.keyDown(2, 1)

driver.scanCycle()

driver.keyUp(2, 1)

driver.scanCycles(2)

driver.skipTime(20)
