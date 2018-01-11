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
#include "KeyboardReport.h"
#include "KPV_Exception.hpp"

namespace kaleidoscope {
namespace python {
   
bool 
   KeyboardReport
      ::isKeycodeActive(uint8_t k) const
{
   if (k <= HID_LAST_KEY) {
      uint8_t bit = 1 << (uint8_t(k) % 8);
      return reportData_.keys[k / 8] & bit;
   }
  
   KP_EXCEPTION("isKeycodeActive: Unknown keycode type " << unsigned(k))
   
  return false;
}

boost::python::list  
   KeyboardReport
      ::getActiveKeycodes() const
{
   boost::python::list activeKeys;
   
   for(uint8_t k = 0; k <= HID_LAST_KEY; ++k) {
      uint8_t bit = 1 << (uint8_t(k) % 8);
      uint8_t keyCode = reportData_.keys[k / 8] & bit;
      if(keyCode) {
         activeKeys.append(k);
      }
   }
   return activeKeys;
}

bool  
   KeyboardReport
      ::isKeyActive(const Key_ &k) const
{
   return this->isKeycodeActive(k.keyCode);
}

bool   
   KeyboardReport
      ::isAnyKeyActive() const
{
   for(int k = 0; k <= HID_LAST_KEY; ++k) {
      uint8_t bit = 1 << (uint8_t(k) % 8);
      if(reportData_.keys[k / 8] & bit) {
         return true;
      }
   }
   
   return false;
}
      
bool
   KeyboardReport
      ::isModifierKeycodeActive(uint8_t k) const
{
   if (k >= HID_KEYBOARD_FIRST_MODIFIER && k <= HID_KEYBOARD_LAST_MODIFIER) {
      k = k - HID_KEYBOARD_FIRST_MODIFIER;
      return !!(reportData_.modifiers & (1 << k));
   }
   
   KP_EXCEPTION("isKeycodeActive: Unknown modifier type " << unsigned(k))
  
   return false;
}  

bool
   KeyboardReport
      ::isModifierActive(const Key &key) const
{
   return this->isModifierKeycodeActive(key.keyCode);
}

bool 
   KeyboardReport
      ::isAnyModifierActive() const
{
   for(uint8_t k = HID_KEYBOARD_FIRST_MODIFIER; k <= HID_KEYBOARD_LAST_MODIFIER; ++k) {
      uint8_t kTmp = k - HID_KEYBOARD_FIRST_MODIFIER;
      if(!!(reportData_.modifiers & (1 << kTmp))) {
         return true;
      }
   }
   return false;
}

boost::python::list  
   KeyboardReport
      ::getActiveModifiers() const
{
   boost::python::list activeModifiers;
   
   for(uint8_t k = HID_KEYBOARD_FIRST_MODIFIER; k <= HID_KEYBOARD_LAST_MODIFIER; ++k) {
      uint8_t kTmp = k - HID_KEYBOARD_FIRST_MODIFIER;
      if(!!(reportData_.modifiers & (1 << kTmp))) {
         activeModifiers.append(k);
      }
   }
   return activeModifiers;
}

bool  
   KeyboardReport
      ::isEmpty() const
{
   return !(this->isAnyModifierActive() || this->isAnyKeyActive());
}
      
void 
   KeyboardReport
      ::setReportData(const HID_KeyboardReport_Data_t &reportData)
{
   memcpy(reportData_.allkeys, reportData.allkeys, sizeof(reportData_));
}

// For each bit set in 'bitfield', output the corresponding string to 'stream'
#define FOREACHBIT(bitfield, stream, str0, str1, str2, str3, str4, str5, str6, str7) \
  if((bitfield) & 1<<0) stream << str0; \
  if((bitfield) & 1<<1) stream << str1; \
  if((bitfield) & 1<<2) stream << str2; \
  if((bitfield) & 1<<3) stream << str3; \
  if((bitfield) & 1<<4) stream << str4; \
  if((bitfield) & 1<<5) stream << str5; \
  if((bitfield) & 1<<6) stream << str6; \
  if((bitfield) & 1<<7) stream << str7;
std::string 
   KeyboardReport
      ::dump() const
{
  std::stringstream keypresses;
  bool anything = false;
  if(reportData_.modifiers) anything = true;
  else for(int i = 0; i < KEY_BYTES; i++) if(reportData_.keys[i]) { anything = true; break; }
  if(!anything) {
    keypresses << "none";
  } else {
    FOREACHBIT(reportData_.modifiers, keypresses,
        "lctrl ", "lshift ", "lalt ", "lgui ",
        "rctrl ", "rshift ", "ralt ", "rgui ")
    FOREACHBIT(reportData_.keys[0], keypresses,
        "NO_EVENT ", "ERROR_ROLLOVER ", "POST_FAIL ", "ERROR_UNDEFINED ",
        "a ", "b ", "c ", "d ")
    FOREACHBIT(reportData_.keys[1], keypresses,
        "e ", "f ", "g ", "h ", "i ", "j ", "k ", "l ")
    FOREACHBIT(reportData_.keys[2], keypresses,
        "m ", "n ", "o ", "p ", "q ", "r ", "s ", "t ")
    FOREACHBIT(reportData_.keys[3], keypresses,
        "u ", "v ", "w ", "x ", "y ", "z ", "1/! ", "2/@ ")
    FOREACHBIT(reportData_.keys[4], keypresses,
        "3/# ", "4/$ ", "5/% ", "6/^ ", "7/& ", "8/* ", "9/( ", "0/) ")
    FOREACHBIT(reportData_.keys[5], keypresses,
        "enter ", "esc ", "del/bksp ", "tab ",
        "space ", "-/_ ", "=/+ ", "[/{ ")
    FOREACHBIT(reportData_.keys[6], keypresses,
        "]/} ", "\\/| ", "#/~ ", ";/: ", "'/\" ", "`/~ ", ",/< ", "./> ")
    FOREACHBIT(reportData_.keys[7], keypresses,
        "//? ", "capslock ", "F1 ", "F2 ", "F3 ", "F4 ", "F5 ", "F6 ")
    FOREACHBIT(reportData_.keys[8], keypresses,
        "F7 ", "F8 ", "F9 ", "F10 ", "F11 ", "F12 ", "prtscr ", "scrolllock ")
    FOREACHBIT(reportData_.keys[9], keypresses,
        "pause ", "ins ", "home ", "pgup ", "del ", "end ", "pgdn ", "r_arrow ")
    FOREACHBIT(reportData_.keys[10], keypresses,
        "l_arrow ", "d_arrow ", "u_arrow ", "numlock ",
        "num/ ", "num* ", "num- ", "num+ ")
    FOREACHBIT(reportData_.keys[11], keypresses,
        "numenter ", "num1 ", "num2 ", "num3 ",
        "num4 ", "num5 ", "num6 ", "num7 ")
    FOREACHBIT(reportData_.keys[12], keypresses,
        "num8 ", "num9 ", "num0 ", "num. ", "\\/| ", "app ", "power ", "num= ")
    FOREACHBIT(reportData_.keys[13], keypresses,
        "F13 ", "F14 ", "F15 ", "F16 ", "F17 ", "F18 ", "F19 ", "F20 ")
    FOREACHBIT(reportData_.keys[14], keypresses,
        "F21 ", "F22 ", "F23 ", "F24 ", "exec ", "help ", "menu ", "sel ")
    FOREACHBIT(reportData_.keys[15], keypresses,
        "stop ", "again ", "undo ", "cut ", "copy ", "paste ", "find ", "mute ")
    FOREACHBIT(reportData_.keys[16], keypresses,
        "volup ", "voldn ", "capslock_l ", "numlock_l ",
        "scrolllock_l ", "num, ", "num= ", "(other) ")
    for(int i = 17; i < KEY_BYTES; i++) {
      // A little imprecise, in two ways:
      //   (1) obviously, "(other)" refers to many distinct keys
      //   (2) this might undercount the number of "other" keys pressed
      // Therefore, if any keys are frequently used, they should be handled above and not via "other"
      if(reportData_.keys[i]) keypresses << "(other) ";
    }
  }

  return keypresses.str();
}

static void initPythonStuff() {
   
   #define EXPORT_METHOD(NAME, DOCSTRING) \
      .def(#NAME, &kaleidoscope::python::KeyboardReport::NAME, DOCSTRING)
      
   boost::python::class_<kaleidoscope::python::KeyboardReport>("KeyboardReport",
      "Provides access to a USB HID key report."
   )
      EXPORT_METHOD(
         isKeycodeActive,
         "Checks it a keycode is active in the key report.\n\n"
         "Args:\n"
         "   keycode (int): The keycode to check.\n\n"
         "Returns:\n"
         "   boolean: True if the given keycode is active in the key report."
      )
      
      EXPORT_METHOD(
         isKeyActive,
         "Checks if a key is active in the key report.\n\n"
         "Args:\n"
         "   key (Key): The key to check.\n\n"
         "Returns:\n"
         "   boolean: True if the given key is active in the key report."
      )
      
      EXPORT_METHOD(
         getActiveKeycodes,
         "Returns the keycodes of all keys that are currently active in the key report.\n\n"
         "Returns:\n"
         "   list: A list of active keycodes."
      )
      
      EXPORT_METHOD(
         isModifierActive,
         "Checks if a modifier is active in the key report.\n\n"
         "Args:\n"
         "   modifier (Key): The modifier to check.\n\n"
         "Returns:\n"
         "   boolean: True if the given modifier is active in the key report."
      )
      
      EXPORT_METHOD(
         isModifierKeycodeActive,
         "Checks if a modifier is active in the key report.\n\n"
         "Args:\n"
         "   modifier (uint8_t): The modifier to check.\n\n"
         "Returns:\n"
         "   boolean: True if the given modifier is active in the key report."
      )
      
      EXPORT_METHOD(
         isAnyModifierActive,
         "Checks if any modifier is active in the key report.\n\n"
         "Returns:\n"
         "   boolean: True if any modifier is active in the key report."
      )
      
      EXPORT_METHOD(
         getActiveModifiers,
         "Returns a list of all keycodes of modifiers that are currently "
         "active in the key report.\n\n"
         "Returns:\n"
         "   list: A list of modifier keycodes."
      )
      
      EXPORT_METHOD(
         isAnyKeyActive,
         "Checks if any key is active in the key report.\n\n"
         "Returns:\n"
         "   boolean: True if any key is active in the key report."
      )
      
      EXPORT_METHOD(
         isEmpty,
         "Checks if the key report is empty, i.e. neither keys nor modifiers are active.\n\n"
         "Returns:\n"
         "   boolean: True if the key report is empty."
      )
      
      EXPORT_METHOD(
         dump,
         "Dumps the key report to stdout."
      )
   ;
}

KALEIDOSCOPE_PYTHON_REGISTER_MODULE(&initPythonStuff, nullptr)

} // namespace python
} // namespace kaleidoscope
