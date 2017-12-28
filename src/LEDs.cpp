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
#include "KPV_Exception.hpp"
#include "Kaleidoscope-Hardware-Virtual.h"

namespace kaleidoscope {
namespace python {
   
static void initPythonStuff() {
   
   KALEIDOSCOPE_PYTHON_MODULE_CONTENT(LEDs)
   
   boost::python::class_<cRGB>("cRGB",
      "A RGB color value."
   )
   .def("getR", boost::python::make_getter(&cRGB::r))
   .def("setR", boost::python::make_setter(&cRGB::r))
   .def("getG", boost::python::make_getter(&cRGB::g))
   .def("setG", boost::python::make_setter(&cRGB::g))
   .def("getB", boost::python::make_getter(&cRGB::b))
   .def("setB", boost::python::make_setter(&cRGB::b))
   ;
   
   boost::python::def("getCrgbAt", &Virtual::getCrgbAt, 
      "Gets LED colors as cRGB at a given matrix position.\n\n"
      "Args:\n"
      "   row (uint8_t): The row of the LED to query.\n"
      "   col (uint8_t): The column of the LED to query.\n\n"
      "Returns:\n"
      "   cRGB: The current color of the LED."
   ).staticmethod("getCrgbAt");
      
   boost::python::def("setCrgbAt", &Virtual::getCrgbAt, 
      "Sets the LED colors as cRGB at a given matrix position.\n\n"
      "Args:\n"
      "   row (uint8_t): The row of the LED to query\n"
      "   col (uint8_t): The column of the LED to query\n"
      "   color (cRGB): The new color of the LED."
   ).staticmethod("getCrgbAt");
}
   
KALEIDOSCOPE_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace kaleidoscope
