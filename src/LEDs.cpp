/* -*- mode: c++ -*-
 * Leidokos-Python -- Wraps Kaleidoscope modules' c++
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

#include "Leidokos-Python.h"
#include "KPV_Exception.hpp"
#include "Kaleidoscope-Hardware-Virtual.h"

extern Virtual KeyboardHardware;

namespace kaleidoscope {
namespace python {
   
static void setCrgbAt(byte row, byte col, cRGB color) {
   KeyboardHardware.setCrgbAt(row, col, color);
}

static cRGB getCrgbAt(byte row, byte col) {
   return KeyboardHardware.getCrgbAt(row, col);
}
   
static void initPythonStuff() {
   
   KALEIDOSCOPE_PYTHON_MODULE_CONTENT(LEDs)
   
   boost::python::class_<cRGB>("cRGB",
      "A RGB color value."
   )
   .def("getRed", boost::python::make_getter(&cRGB::r))
   .def("setRed", boost::python::make_setter(&cRGB::r))
   .def("getGreen", boost::python::make_getter(&cRGB::g))
   .def("setGreen", boost::python::make_setter(&cRGB::g))
   .def("getBlue", boost::python::make_getter(&cRGB::b))
   .def("setBlue", boost::python::make_setter(&cRGB::b))
   ;
   
   boost::python::def("getCrgbAt", &getCrgbAt, 
      "Gets LED colors as cRGB at a given matrix position.\n\n"
      "Args:\n"
      "   row (uint8_t): The row of the LED to query.\n"
      "   col (uint8_t): The column of the LED to query.\n\n"
      "Returns:\n"
      "   cRGB: The current color of the LED."
   );
      
   boost::python::def("setCrgbAt", &setCrgbAt, 
      "Sets the LED colors as cRGB at a given matrix position.\n\n"
      "Args:\n"
      "   row (uint8_t): The row of the LED to query\n"
      "   col (uint8_t): The column of the LED to query\n"
      "   color (cRGB): The new color of the LED."
   );
}
   
KALEIDOSCOPE_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace kaleidoscope
