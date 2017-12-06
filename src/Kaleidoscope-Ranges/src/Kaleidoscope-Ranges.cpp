/* -*- mode: c++ -*-
 * Kaleidoscope-Python -- Wraps Kaleidoscope modules' c++
 *    code to be available in Python programs.
 * Copyright (C) 2017 noseglasses <shinynoseglasses@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "Kaleidoscope-Python.h"

#include <Kaleidoscope-Ranges.h>

namespace kaleidoscope {
namespace python {
   
#define FOR_ALL_RANGES(FUNC) \
   FUNC(FIRST) \
   FUNC(KALEIDOSCOPE_FIRST) \
   FUNC(OS_FIRST) \
   FUNC(OSM_FIRST) \
   FUNC(OSM_LAST) \
   FUNC(OSL_FIRST) \
   FUNC(OSL_LAST) \
   FUNC(OS_LAST) \
   FUNC(DU_FIRST) \
   FUNC(DUM_FIRST) \
   FUNC(DUM_LAST) \
   FUNC(DUL_FIRST) \
   FUNC(DUL_LAST) \
   FUNC(DU_LAST) \
   FUNC(TD_FIRST) \
   FUNC(TD_LAST) \
   FUNC(LEAD_FIRST) \
   FUNC(LEAD_LAST) \
   FUNC(CYCLE) \
   FUNC(SYSTER) \
   FUNC(TT_FIRST) \
   FUNC(TT_LAST) \
   FUNC(STENO_FIRST) \
   FUNC(STENO_LAST) \
   FUNC(SAFE_START) \
   FUNC(KALEIDOSCOPE_SAFE_START)

#define DEFINE_RANGES(RANGE) \
   static uint16_t range_##RANGE() { return kaleidoscope::ranges::RANGE; }
   
FOR_ALL_RANGES(DEFINE_RANGES)

static void registerPythonStuff() {
   
   KALEIDOSCOPE_PYTHON_MODULE_CONTENT(ranges)

   #define EXPORT_RANGES(RANGE) \
      boost::python::def(#RANGE, &kaleidoscope::python::range_##RANGE, \
         "Returns the range \"" #RANGE "\".\n\n" \
         "Returns:\n" \
         "   uint16_t: The range \"" #RANGE "\"." \
      );
      
   FOR_ALL_RANGES(EXPORT_RANGES)
}
      
KALEIDOSCOPE_PYTHON_REGISTER_MODULE(registerPythonStuff)

} // namespace python
} // namespace kaleidoscope
