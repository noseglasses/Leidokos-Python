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

#include "Kaleidoscope.h"

#include "KPV_Logging.h"

#include <iostream>

namespace leidokos {
namespace python {
   
#define FOR_N(OP) \
   OP(0) \
   OP(1) \
   OP(2) \
   OP(3) \
   OP(4) \
   OP(5) \
   OP(6) \
   OP(7) \
   OP(8) \
   OP(9) 
   
#define KP_MAX_HOOKS 10
static boost::python::object eventHandlerHooks[KP_MAX_HOOKS];
static boost::python::object loopHooks[KP_MAX_HOOKS];

#define DEFINE_EVENT_HANDLER_HOOK(N) \
   static Key eventHandlerHook_##N(Key mappedKey, byte row, byte col, uint8_t keyState) { \
      KPV_LOG("Trying to call event handler hook " << N) \
      if(eventHandlerHooks[N]) { \
         KPV_LOG("Calling event handler hook " << N) \
         return boost::python::extract<Key>(eventHandlerHooks[N].attr("eventHandlerHook")(mappedKey, row, col, keyState)); \
      } \
      \
      return mappedKey;\
   }
   
FOR_N(DEFINE_EVENT_HANDLER_HOOK)
   
#define DEFINE_LOOP_HOOK(N) \
   static void loopHook_##N(bool postClear) { \
      if(loopHooks[N]) { \
         loopHooks[N].attr("loopHook")(postClear); \
      } \
   }
FOR_N(DEFINE_LOOP_HOOK)
   
static void replaceEventHandlerHook(
               boost::python::object oldHook,
               boost::python::object newHook)
{
   for(int i = 0; i < KP_MAX_HOOKS; ++i) {
      if(eventHandlerHooks[i] == oldHook) {
         eventHandlerHooks[i] = newHook;
         break;
      }
   }
}

static void useEventHandlerHook(
               boost::python::object hook)
{
   KPV_LOG("Registering event handler hook")
   for(int i = 0; i < KP_MAX_HOOKS; ++i) {
      if(!eventHandlerHooks[i]) {
         KPV_LOG("Setting event handler hook " << i)
         eventHandlerHooks[i] = hook;
         break;
      }
   }
}

static void replaceLoopHook(
               boost::python::object oldHook,
               boost::python::object newHook)
{
   for(int i = 0; i < KP_MAX_HOOKS; ++i) {
      if(loopHooks[i] == oldHook) {
         loopHooks[i] = newHook;
         break;
      }
   }
}

static void useLoopHook(
               boost::python::object hook)
{
   for(int i = 0; i < KP_MAX_HOOKS; ++i) {
      if(!loopHooks[i]) {
         loopHooks[i] = hook;
         break;
      }
   }
}
   
static void exportPython() {
   
   // Functions and methods from Kaleidoscope/Kaleidoscope.h
   //
   #define EXPORT_KALEIDOSCOPE_STATIC_METHOD(NAME, DOCSTRING) \
      .def(#NAME, &NAME, DOCSTRING).staticmethod(#NAME)
   boost::python::class_<Kaleidoscope_>("Kaleidoscope_",
         "The main class of the firmware")
   .def("replaceEventHandlerHook", &leidokos::python::replaceEventHandlerHook, 
      "Replaces an event handler hook.\n\n"
      "Args:\n"
      "   oldHook (python object): The old event handler hook.\n"
      "   newHook (python object): The new event handler hook.\n"
   ).staticmethod("replaceEventHandlerHook")
   
   .def("useEventHandlerHook", &leidokos::python::useEventHandlerHook, 
      "Adds an event handler hook.\n\n"
      "Args:\n"
      "   hook (python object): The event handler hook."
   ).staticmethod("useEventHandlerHook")
      
   .def("replaceLoopHook", &leidokos::python::replaceLoopHook, 
      "Replaces a loop hook.\n\n"
      "Args:\n"
      "   oldHook (python object): The old loop hook.\n"
      "   newHook (python object): The new event handler hook.\n"
   ).staticmethod("replaceLoopHook")
   
   .def("useLoopHook", &leidokos::python::useLoopHook, 
      "Adds a loop hook.\n\n"
      "Args:\n"
      "   hook (python object): The loop hook."
   ).staticmethod("useLoopHook")
   ;
   
#define REGISTER_HOOK(N) \
   Kaleidoscope_::useEventHandlerHook(&eventHandlerHook_##N); \
   Kaleidoscope_::useLoopHook(&loopHook_##N);
   
   FOR_N(REGISTER_HOOK)
}

static void finalizePython()
{
   for(int i = 0; i < KP_MAX_HOOKS; ++i) {
      eventHandlerHooks[i] = boost::python::object();
      loopHooks[i] = boost::python::object();
   }
}
      
LEIDOKOS_PYTHON_EXPORT(&exportPython, &finalizePython)

} // namespace python
} // namespace leidokos
