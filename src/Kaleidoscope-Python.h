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
   /* map the IO namespace to a sub-module \
      make "from kaleidoscope.MODULE_NAME import <whatever>" work \
   */ \
   boost::python::object MODULE_NAME##Module( \
      boost::python::handle<>( \
         boost::python::borrowed( \
            PyImport_AddModule(STRINGIZE(KALEIDOSCOPE_PYTHON_PACKAGE_NAME) \
               "." #MODULE_NAME) \
         ) \
      ) \
   ); \
   \
   /* make "from mypackage import class1" work \
   boost::python::scope().attr("class1") = class1Module; */ \
   \
   /* set the current scope to the new sub-module \
   */ \
   boost::python::scope io_scope = MODULE_NAME##Module;

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
