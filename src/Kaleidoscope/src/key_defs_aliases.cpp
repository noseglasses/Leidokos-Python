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

#include "key_defs_aliases.h"

namespace leidokos {
namespace python {
   
#define FOR_ALL_KEY_ALIASES(FUNC) \
   FUNC(Space) \
   FUNC(LBracket) \
   FUNC(LArrow) \
   FUNC(LCtrl) \
   FUNC(LShift) \
   FUNC(LAlt) \
   FUNC(LGui) \
   FUNC(RBracket) \
   FUNC(RArrow) \
   FUNC(RCtrl) \
   FUNC(RShift) \
   FUNC(RAlt) \
   FUNC(RGui) \
   FUNC(Esc) \
    \
   FUNC(LSquareBracket) \
   FUNC(RSquareBracket) \
   \
   FUNC(DnArrow) \
   \
   FUNC(LeftParen) \
   FUNC(RightParen) \
   FUNC(LeftCurlyBracket) \
   FUNC(RightCurlyBracket) \
   \
   FUNC(Pipe)
   
#define DEFINE_KEY_FUNCTIONS(KEY) \
   static Key_ k_##KEY() { return Key_##KEY; }
   
FOR_ALL_KEY_ALIASES(DEFINE_KEY_FUNCTIONS)

static void exportPython() {
   
   #define EXPORT_KEY_FUNCTIONS(KEY) \
      boost::python::def("key"#KEY, &leidokos::python::k_##KEY, \
         "Returns the key \"" #KEY "\".\n\n" \
         "Returns:\n" \
         "   Key: The key \"" #KEY "\"." \
      );
      
   FOR_ALL_KEY_ALIASES(EXPORT_KEY_FUNCTIONS)
}
      
LEIDOKOS_PYTHON_EXPORT(&exportPython, nullptr)

} // namespace python
} // namespace leidokos
