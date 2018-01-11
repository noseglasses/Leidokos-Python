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

#include "key_defs_sysctl.h"

namespace kaleidoscope {
namespace python {
   
#define FOR_ALL_SYSCTL(FUNC) \
FUNC(PowerDown) \
FUNC(Sleep) \
FUNC(WakeUp) \
FUNC(ContextMenu) \
FUNC(MainMenu) \
FUNC(AppMenu) \
FUNC(MenuHelp) \
FUNC(MenuExit) \
FUNC(MenuSelect) \
FUNC(MenuRight) \
FUNC(MenuLeft) \
FUNC(MenuUp) \
FUNC(MenuDown) \
FUNC(ColdRestart) \
FUNC(WarmRestart) \
FUNC(DPadUp) \
FUNC(DPadDown) \
FUNC(DPadRight) \
FUNC(DPadLeft) \
\
FUNC(Dock) \
FUNC(Undock) \
FUNC(Setup) \
FUNC(Break) \
FUNC(DebuggerBreak) \
FUNC(ApplicationBreak) \
FUNC(ApplicationDebuggerBreak) \
FUNC(SpeakerMute) \
FUNC(Hibernate) \
\
FUNC(DisplayInvert) \
FUNC(DisplayInternal) \
FUNC(DisplayExternal) \
FUNC(DisplayBoth) \
FUNC(DisplayDual) \
FUNC(DisplayToggleIntSlashExt) \
FUNC(DisplaySwapPrimarySlashSecondary) \
FUNC(DisplayLCDAutoscale)

#define DEFINE_SYSCTL(KEY) \
   static Key_ system_##KEY() { return System_##KEY; }
   
FOR_ALL_SYSCTL(DEFINE_SYSCTL)

static void initPythonStuff() {
   
   #define EXPORT_SYSCTL(KEY) \
      boost::python::def("keySystem"#KEY, &kaleidoscope::python::system_##KEY, \
         "Returns the system control key \"" #KEY "\".\n\n" \
         "Returns:\n" \
         "   Key: The system control key \"" #KEY "\"." \
      );
      
   FOR_ALL_SYSCTL(EXPORT_SYSCTL)
}
      
LEIDOKOS_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace kaleidoscope
