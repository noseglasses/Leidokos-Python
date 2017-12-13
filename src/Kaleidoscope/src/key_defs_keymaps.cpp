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

#include "key_defs_keymaps.h"

namespace kaleidoscope {
namespace python {
   
#define FOR_ALL_KEYMAPS(FUNC) \
   FUNC(Keymap0) \
   FUNC(Keymap1) \
   FUNC(Keymap2) \
   FUNC(Keymap3) \
   FUNC(Keymap4) \
   FUNC(Keymap5) \
   FUNC(Keymap0_Momentary) \
   FUNC(Keymap1_Momentary) \
   FUNC(Keymap2_Momentary) \
   FUNC(Keymap3_Momentary) \
   FUNC(Keymap4_Momentary) \
   FUNC(Keymap5_Momentary) \
   \
   FUNC(KeymapNext_Momentary) \
   FUNC(KeymapPrevious_Momentary) \
   
static Key keyLockLayer(uint8_t layerId) {
   return LockLayer(layerId);
} 
static Key keyUnlockLayer(uint8_t layerId) {
   return UnlockLayer(layerId);
}

static Key keyShiftToLayer(uint8_t layerId) {
   return ShiftToLayer(layerId);
}

#define DEFINE_KEYMAPS(KEY) \
   static Key_ k_##KEY() { return Key_##KEY; }
   
FOR_ALL_KEYMAPS(DEFINE_KEYMAPS)

static void initPythonStuff() {
   
   #define EXPORT_KEYMAPS(KEY) \
      boost::python::def("key"#KEY, &kaleidoscope::python::k_##KEY, \
         "Returns the key \"" #KEY "\".\n\n" \
         "Returns:\n" \
         "   Key: The key \"" #KEY "\"." \
      );
      
   FOR_ALL_KEYMAPS(EXPORT_KEYMAPS)
   
   boost::python::def("keyLockLayer", &kaleidoscope::python::keyLockLayer,
      "Returns a control key that locks a specific layer.\n\n"
      "Args:\n"
      "   layerId (int): The layer id\n\n"
      "Returns:\n" \
      "   Key: The layer lock key."
   );
   
   boost::python::def("keyUnlockLayer", &kaleidoscope::python::keyUnlockLayer,
      "Returns a control key that unlocks a specific layer.\n\n"
      "Args:\n"
      "   layerId (int): The layer id\n\n"
      "Returns:\n" \
      "   Key: The layer unlock key."
   );
   
   boost::python::def("keyShiftToLayer", &kaleidoscope::python::keyShiftToLayer,
      "Returns a control key that shifts to a specific layer.\n\n"
      "Args:\n"
      "   layerId (int): The layer id\n\n"
      "Returns:\n" \
      "   Key: The layer shift key."
   );
}
      
KALEIDOSCOPE_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace kaleidoscope
