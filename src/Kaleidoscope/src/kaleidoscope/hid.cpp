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

#include "kaleidoscope/hid.h"

namespace kaleidoscope {
namespace python {
   
static void initPythonStuff() {
   
   LEIDOKOS_PYTHON_MODULE_CONTENT(hid)

   #define EXPORT_FUNCTION(NAME, DOCSTRING) \
      boost::python::def(#NAME, &kaleidoscope::hid::NAME, DOCSTRING);

   EXPORT_FUNCTION(
      initializeKeyboard,
      "Initializes the keyboard."
   )
   EXPORT_FUNCTION(
      pressKey,
      "Press a given key.\n\n"
      "Args:\n"
      "   mappedKey (Key): The mapped key to press."
   )
   EXPORT_FUNCTION(
      releaseKey,
      "Release a given key.\n\n"
      "Args:\n"
      "   mappedKey (Key): The mapped key to release."
   )
   EXPORT_FUNCTION(
      releaseAllKeys,
      "Releases all keys."
   )
   EXPORT_FUNCTION(
      pressRawKey,
      "Presses a raw key.\n\n"
      "Args:\n"
      "   mappedKey (Key): The mapped key to press."
   )
   EXPORT_FUNCTION(
      releaseRawKey,
      "Presses a raw key.\n\n"
      "Args:\n"
      "   mappedKey (Key): The mapped key to release."
   )
   EXPORT_FUNCTION(
      sendKeyboardReport,
      "Flushes any pending keyboard report."
   )
   EXPORT_FUNCTION(
      isModifierKeyActive,
      "Checks if a modifier is active.\n\n"
      "Args:\n"
      "   mappedKey (Key): The mapped key to interpret as modifier.\n\n"
      "Returns:\n"
      "   boolean: True if the modifier is active, False otherwise."
   )
   EXPORT_FUNCTION(
      isModifierKeyActive,
      "Checks if a modifier was active.\n\n"
      "Args:\n"
      "   mappedKey (Key): The mapped key to interpret as modifier.\n\n"
      "Returns:\n"
      "   boolean: True if the modifier was active, False otherwise."
   )
   EXPORT_FUNCTION(
      getKeyboardLEDs,
      "Returns the keyboard LEDs.\n\n"
      "Returns:\n"
      "   uint8_t: The LEDs."
   )
   EXPORT_FUNCTION(
      initializeConsumerControl,
      "Initializes the consumer control."
   )
   EXPORT_FUNCTION(
      pressConsumerControl,
      "Presses a consumer control key.\n\n"
      "Args:\n"
      "   mappedKey (Key): The consumer control key."
   )
   EXPORT_FUNCTION(
      releaseConsumerControl,
      "Releases a consumer control key.\n\n"
      "Args:\n"
      "   mappedKey (Key): The consumer control key."
   )
   EXPORT_FUNCTION(
      initializeSystemControl,
      "Initializes the system control."
   )
   EXPORT_FUNCTION(
      pressSystemControl,
      "Presses a system control key.\n\n"
      "Args:\n"
      "   mappedKey (Key): The system control key."
   )
   EXPORT_FUNCTION(
      releaseSystemControl,
      "Releases a system control key.\n\n"
      "Args:\n"
      "   mappedKey (Key): The system control key."
   )
   EXPORT_FUNCTION(
      initializeMouse,
      "Initializes the mouse."
   )
   EXPORT_FUNCTION(
      moveMouse,
      "Moves the mouse.\n\n"
      "Args:\n"
      "   x (signed char): The x movement.\n"
      "   y (signed char): The y movement.\n"
      "   vWheel (signed char): The vertical wheel movement."
      "   hWheel (signed char): The horizontal wheel movement."
   )
   EXPORT_FUNCTION(
      clickMouseButtons,
      "Clicks a given set of mouse buttons.\n\n"
      "Args:\n"
      "   buttons (uint8_t): The buttons clicked."
   )
   EXPORT_FUNCTION(
      pressMouseButtons,
      "Activates a given set of mouse buttons.\n\n"
      "Args:\n"
      "   buttons (uint8_t): The buttons activated."
   )
   EXPORT_FUNCTION(
      releaseMouseButtons,
      "Deactivates a given set of mouse buttons.\n\n"
      "Args:\n"
      "   buttons (uint8_t): The buttons deactivated."
   )
   EXPORT_FUNCTION(
      initializeAbsoluteMouse,
      "Initializes the mouse absolutely."
   )
   EXPORT_FUNCTION(
      moveAbsoluteMouseTo,
      "Moves the mouse to a given position.\n\n"
      "Args:\n"
      "   x (signed char): The x position.\n"
      "   y (signed char): The y position.\n"
      "   wheel (signed char): The wheel position."
   )
   EXPORT_FUNCTION(
      clickAbsoluteMouseButtons,
      "Clicks a given set of mouse buttons.\n\n"
      "Args:\n"
      "   buttons (uint8_t): The buttons clicked."
   )
   EXPORT_FUNCTION(
      pressAbsoluteMouseButtons,
      "Activates a given set of mouse buttons.\n\n"
      "Args:\n"
      "   buttons (uint8_t): The buttons activated."
   )
   EXPORT_FUNCTION(
      releaseAbsoluteMouseButtons,
      "Deactivates a given set of mouse buttons.\n\n"
      "Args:\n"
      "   buttons (uint8_t): The buttons deactivated."
   )
   ;
}
      
LEIDOKOS_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace kaleidoscope
