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

#ifndef LEIDOKOS_PYTHON_H
#define LEIDOKOS_PYTHON_H

// Important: Do not change the order of the following headers. Else
//            there are strange boost symbol related compile errors.
//
#include <cmath>
#include <boost/python.hpp>

// Starting from here, the order of includes does not matter any further.

#include "Kaleidoscope-Hardware-Virtual.h"
#include "Leidokos-Python.h"
#include "VirtualHID/Keyboard.h"

#include "key_defs.h"

#include <string>
#include <vector>

namespace leidokos {
namespace python {
   
typedef void (*PluginRegistrationCallback)();
typedef std::vector<PluginRegistrationCallback> PluginRegistrationCallbacks;
PluginRegistrationCallbacks &pluginRegistrationCallbacks();

typedef void (*PluginFinalizationCallback)();
typedef std::vector<PluginFinalizationCallback> PluginFinalizationCallbacks;
PluginFinalizationCallbacks &pluginFinalizationCallbacks();

#define LEIDOKOS_PYTHON_PACKAGE_NAME kaleidoscope

#define __STRINGIZE(S) #S
#define STRINGIZE(S) __STRINGIZE(S)

#define CONCAT(S1, S2) S1##S2

#define __LEIDOKOS_PYTHON_MODULE_CONTENT(MODULE_NAME, COUNTER) \
   \
   namespace py = boost::python; \
   std::string CONCAT(nested_name, COUNTER) = py::extract<std::string>(py::scope().attr("__name__") + "." #MODULE_NAME); \
   py::object CONCAT(nested_module, COUNTER)(py::handle<>(py::borrowed(PyImport_AddModule(CONCAT(nested_name, COUNTER).c_str())))); \
   py::scope().attr(#MODULE_NAME) = CONCAT(nested_module, COUNTER); \
   py::scope CONCAT(parent, COUNTER) = CONCAT(nested_module, COUNTER);
   
#define LEIDOKOS_PYTHON_MODULE_CONTENT(MODULE_NAME) \
   __LEIDOKOS_PYTHON_MODULE_CONTENT(MODULE_NAME, __COUNTER__)

#define LEIDOKOS_PYTHON_EXPORT( \
               REGISTRATION_FUNCTION_PTR, \
               FINALIZATION_FUNCTION_PTR \
) \
   \
   static bool __registerModule() { \
      ::leidokos::python::pluginRegistrationCallbacks().push_back(REGISTRATION_FUNCTION_PTR); \
      auto finFuncPtr = FINALIZATION_FUNCTION_PTR; \
      if((bool)finFuncPtr) { \
         ::leidokos::python::pluginFinalizationCallbacks().push_back(finFuncPtr); \
      } \
      return true; \
   }\
   \
   __attribute__((unused)) static bool __moduleRegistered = __registerModule();
   
} // namespace python
} // namespace leidokos

#endif
