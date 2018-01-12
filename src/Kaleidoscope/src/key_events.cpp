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

#include "key_events.h"

namespace leidokos {
namespace python {

static void initPythonStuff() {

   boost::python::def("handleKeyswitchEvent", &handleKeyswitchEvent,
      "Calls the key switch handling function.\n\n"
      "Args:\n"
      "   mappedKey (Key): The mapped key to consider.\n"
      "   row (byte): The keyboard row.\n"
      "   col (byte): The keyboard colum.\n"
      "   keyState (uint8_t): The key state.\n"
   );
}
      
LEIDOKOS_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace leidokos
