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

kaleidoscope.keyDown(2, 1)

# The assertions are evaluated in the next loop cycle
#
test.addAssertions([NthReportInCycle(0), 
               NthCycle(0),
               KeyActive(kaleidoscope.Key.A()),
               KeyActive(kaleidoscope.Key.B()),
               ModifierActive(kaleidoscope.Key.SHIFT_HELD())
               ])

kaleidoscope.loop()

test = None
