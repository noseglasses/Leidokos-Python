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

#include KALEIDOSCOPE_HARDWARE_H

#include "layers.h"

namespace kaleidoscope {
namespace python {
   
static void initPythonStuff() {
   
   #define EXPORT_LAYER_STATIC_METHOD(NAME, DOCSTRING) \
      .def(#NAME, &Layer_::NAME, DOCSTRING).staticmethod(#NAME)
      
   boost::python::class_<Layer_>("Layer",
      "Provides access to layered keymaps."
   )
      EXPORT_LAYER_STATIC_METHOD(
         lookup,
         "Lookup a Key at a given position in the overall keymap.\n\n"
         "Args:\n"
         "   row (int): The keymap row.\n"
         "   col (int): The keymap col.\n\n"
         "Returns:\n"
         "   Key: The key present at that the given position in the keymap.")
      
      EXPORT_LAYER_STATIC_METHOD(
         lookupOnActiveLayer,
         "Lookup a Key at a given position in the current layer mapping.\n\n"
         "Args:\n"
         "   row (int): The keymap row.\n"
         "   col (int): The keymap col.\n\n"
         "Returns:\n"
         "   Key: The key present at that the given position in the active layer.")
      
      EXPORT_LAYER_STATIC_METHOD(
         lookupActiveLayer,
         "Lookup the active layer of a Key at a given position in the current layer mapping.\n\n"
         "Args:\n"
         "   row (int): The keymap row.\n"
         "   col (int): The keymap col.\n\n"
         "Returns:\n"
         "   uint8_t: The layer id.")
         
      EXPORT_LAYER_STATIC_METHOD(
         on,
         "Enables a layer.\n\n"
         "Args:\n"
         "   layer (int): The layer to enable.")
      
      EXPORT_LAYER_STATIC_METHOD(
         off,
         "Disables a layer.\n\n"
         "Args:\n"
         "   layer (int): The layer to disable.")
      
      EXPORT_LAYER_STATIC_METHOD(move,
         "Enables a single layer (while disabling all others).\n\n"
         "Args:\n"
         "   layer (int): The layer to enable.")
      
      EXPORT_LAYER_STATIC_METHOD(
         top,
         "Retreives the id of the current highest layer.\n\n"
         "Returns:\n"
         "   int: The id of the current highest layer.")
      
      EXPORT_LAYER_STATIC_METHOD(
         next,
         "Turns the next higher layer into the highest layer and activates it.\n\n")
      
      EXPORT_LAYER_STATIC_METHOD(
         previous,
         "Turns the next lower layer into the highest layer and disables the "
         "foremost highest layer.\n\n")
      
      EXPORT_LAYER_STATIC_METHOD(
         isOn,
         "Checks it a given layer is currently enabled.\n\n"
         "Args:\n"
         "   layer (int): The layer to check.\n\n"
         "Returns:\n"
         "   boolean: True if the given layer is enabled, False otherwise.")
      
      EXPORT_LAYER_STATIC_METHOD(
         getLayerState,
         "Retreives the current layer state.\n\n"
         "Returns:\n"
         "   unsigned int: The current layer state coded as a 32 bit value.")
      
      EXPORT_LAYER_STATIC_METHOD(
         eventHandler,
         "Calls the event handler for a mapped key.\n\n"
         "Args:\n"
         "   mappedKey (Key): The mapped key to pass to the event handler.\n"
         "   row (int): The keymap row associated with the mapped key.\n"
         "   col (int): The keymap column associated with the mapped key.\n"
         "   keyState (int): The key state to pass to the event handler.\n\n"
         "Returns:\n"
         "   Key: Key_NoKey if the event handler was called, mappedKey otherwise.")
      
      EXPORT_LAYER_STATIC_METHOD(
         getKeyFromPROGMEM,
         "Reads a Key at a given position on a given layer.\n\n"
         "Args:\n"
         "   layer (int): The layer id\n"
         "   row (int): The keymap row associated with the mapped key.\n"
         "   col (int): The keymap column associated with the mapped key.\n"
         "Returns:\n"
         "   Key: The key found in the keymap")
      
      EXPORT_LAYER_STATIC_METHOD(
         updateLiveCompositeKeymap,
         "Updates the live composite keymap at a given position.\n\n"
         "Args:\n"
         "   row (int): The keymap row.\n"
         "   col (int): The keymap column.\n")
      
      EXPORT_LAYER_STATIC_METHOD(
         updateActiveLayers,
         "Updates the active layers.")
      
      // As there are two overloaded versions of 
      // defaultLayer that are actually a getter and a setter, we have 
      // to point the compiler to the different versions of the functions
      // by casting to the different function pointer types
      //
      .def("getDefaultLayer", static_cast< 
            uint8_t(*)()
         >(&Layer_::defaultLayer),
         "Returns the default layer.\n\n"
         "Returns:\n"
         "   int: The default layer ID"
      ).staticmethod("getDefaultLayer")
      
      .def("setDefaultLayer", static_cast< 
            void(*)(uint8_t)
         >(&Layer_::defaultLayer),
         "Sets the default layer.\n\n"
         "Args:\n"
         "   layer (int): The new default layer ID"
      ).staticmethod("setDefaultLayer")
    ;
}

KALEIDOSCOPE_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace kaleidoscope
