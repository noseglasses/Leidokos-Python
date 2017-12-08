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

#ifndef KALEIDOSCOPE_PYTHON_H
#define KALEIDOSCOPE_PYTHON_H

#include <boost/python.hpp>

#include "Kaleidoscope-Hardware-Virtual.h"
#include "Kaleidoscope-Python.h"
#include "VirtualHID/Keyboard.h"

#include "key_defs.h"

#include <string>

namespace kaleidoscope {
namespace python {
   
typedef void (*PluginRegistrationCallback)();

typedef std::vector<PluginRegistrationCallback> PluginRegistrationCallbacks;

PluginRegistrationCallbacks &pluginRegistrationCallbacks();

#define KALEIDOSCOPE_PYTHON_PACKAGE_NAME _kaleidoscope

#define STRINGIZE(S) #S

#define KALEIDOSCOPE_PYTHON_MODULE_CONTENT(MODULE_NAME) \
   \
   namespace py = boost::python; \
   std::string nested_name = py::extract<std::string>(py::scope().attr("__name__") + "." #MODULE_NAME); \
   py::object nested_module(py::handle<>(py::borrowed(PyImport_AddModule(nested_name.c_str())))); \
   py::scope().attr(#MODULE_NAME) = nested_module; \
   py::scope parent = nested_module;

#define KALEIDOSCOPE_PYTHON_REGISTER_MODULE(REGISTRATION_FUNCTION) \
   \
   static bool __registerModule() { \
      pluginRegistrationCallbacks().push_back(&REGISTRATION_FUNCTION); \
      return true; \
   }\
   \
   __attribute__((unused)) static bool __moduleRegistered = __registerModule();
   
} // namespace python
} // namespace kaleidoscope

#endif
