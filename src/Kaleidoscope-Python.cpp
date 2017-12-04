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
#include "KPV_Key_Alias.h"

#include "layers.h"
#include "virtual_io.h"
#include "VirtualHID/Keyboard.h"

#include <string.h>

#include <iostream>
#include <sstream>

// Also defined by Kaleidoscope-Hardware-Virtual
//
void initVariant() __attribute__((weak));
void setup(void);

unsigned long millis(void) {
   return kaleidoscope::PYTHON::API::getMillis();
}

extern Virtual KeyboardHardware;

namespace kaleidoscope {
namespace PYTHON {
   
unsigned long API::millis_ = 0;
   
API::KeyboardReportConsumer API::keyboardReportConsumer_;

extern std::string getVersionString();
   
void 
   API
      ::init()
{
   KeyboardHardware.setEnableReadMatrix(false);
   
   Keyboard.setKeyboardReportConsumer(keyboardReportConsumer_);
   
	initVariant();

	setup();
}   

void 
   API
      ::scanCycle()
{
   ::loop();
   nextCycle();
}

void  
   API
      ::tap(byte row, byte col)
{
   KeyboardHardware.setKeystate(row, col, Virtual::TAP);
}

void  
   API
      ::keyDown(byte row, byte col)
{
   KeyboardHardware.setKeystate(row, col, Virtual::PRESSED);
}

void  
   API
      ::keyUp(byte row, byte col)
{
   KeyboardHardware.setKeystate(row, col, Virtual::NOT_PRESSED);
}

void  
   API
      ::clearAllKeys()
{
   for(byte row = 0; row < ROWS; row++) {
      for(byte col = 0; col < COLS; col++) {
         KeyboardHardware.setKeystate(row, col, Virtual::NOT_PRESSED);
      }
   }
}

void   
   API
      ::setMillis(unsigned long millis)
{
   millis_ = millis;
}

unsigned long   
   API
      ::getMillis()
{
   return millis_;
}
      
void   
   API
      ::setKeyboardReportCallback(boost::python::object func)
{
   keyboardReportConsumer_.keyboardReportCallback_ = func;
}

void 
   API::KeyboardReportConsumer
      ::processKeyboardReport(
                           const HID_KeyboardReport_Data_t &reportData)
{
   this->keyboardReport_.setReportData(reportData);
   
   bool reportCallbackCalled = false;
   
   #define REPORT_CALLBACK_METHOD "processReport"
   
   if(this->keyboardReportCallback_) {
      
      boost::python::object processReport 
         = this->keyboardReportCallback_.attr(REPORT_CALLBACK_METHOD);
      
      if(processReport) {
         processReport(this->keyboardReport_);
         reportCallbackCalled = true;
      }
      else {
         std::cerr << "Error: Unable to find \"" REPORT_CALLBACK_METHOD "\" "
                        "method of callable python object" << std::endl;
      }
   }
   
   if(!reportCallbackCalled) {
      std::cerr << "Error: No report callback available" << std::endl;
      abort();
   }
}

bool 
   KeyboardReport
      ::isKeycodeActive(uint8_t k) const
{
  if (k <= HID_LAST_KEY) {
     uint8_t bit = 1 << (uint8_t(k) % 8);
     return reportData_.keys[k / 8] & bit;
  }
  return false;
}
 
bool  
   KeyboardReport
      ::isKeyActive(const Key_ &k) const
{
   return this->isKeycodeActive(k.keyCode);
}
      
bool
   KeyboardReport
      ::isModifierActive(uint8_t k) const
{
   if (k >= HID_KEYBOARD_FIRST_MODIFIER && k <= HID_KEYBOARD_LAST_MODIFIER) {
      k = k - HID_KEYBOARD_FIRST_MODIFIER;
      return !!(reportData_.modifiers & (1 << k));
   }
   return false;
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

} // namespace PYTHON
} // namespace kaleidoscope

using namespace boost::python;

#define DEFINE_MODIFIER_FUNCTIONS(MOD) \
   static Key_ m_##MOD(const Key_ &key) { return MOD(key); }
   
FOR_ALL_MODIFIERS(DEFINE_MODIFIER_FUNCTIONS)

#define DEFINE_HELD_MODIFIER_FUNCTIONS(MOD) \
   static uint8_t hm_##MOD() { return MOD; }
   
FOR_ALL_HELD_MODIFIERS(DEFINE_HELD_MODIFIER_FUNCTIONS)

#define DEFINE_KEY_FUNCTIONS(KEY) \
   static Key_ k_##KEY() { return Key_##KEY; }

FOR_ALL_KEYS(DEFINE_KEY_FUNCTIONS)

static const char *keycodeToName(uint8_t keycode) {
   
   switch(keycode) {
      
#define DEFINE_KEY_CASE(KEY) \
      case (Key_##KEY).keyCode: \
         return #KEY; \
         break;
      
   FOR_ALL_NORMAL_KEYS(DEFINE_KEY_CASE) 
   
   // Keycodes for some keys are redundant
   //
//    FOR_ALL_KEYMAP_KEYS(DEFINE_KEY_CASE) 
   //FOR_ALL_SIGNAL_KEYS(DEFINE_KEY_CASE) 
//    FOR_ALL_SPECIAL_KEYS(DEFINE_KEY_CASE)
   }

   return "";
}

static const char *keyToName(const Key &key) {
   return keycodeToName(key.keyCode);
}

static const char *modifierToName(uint8_t modifier) {
   
   switch(modifier) {
      
#define DEFINE_MOD_CASE(MOD) \
      case MOD: \
         return #MOD; \
         break;
      
      FOR_ALL_HELD_MODIFIERS(DEFINE_MOD_CASE)
   }

   return "";
}

BOOST_PYTHON_MODULE(_kaleidoscope)
{
   #define EXPORT_LAYER_STATIC_METHOD(NAME, DOCSTRING) \
      .def(#NAME, &Layer_::NAME, DOCSTRING).staticmethod(#NAME)
      
   class_<Layer_>("Layer",
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
    
   class_<Key_>("Key",
      "Provides functionality to deal with and to represent keys."
   )
      .def(self == uint16_t())
      .def(self == Key_())
//       .def(self = uint16_t())
      .def(self != Key_())
      .def(self >= uint16_t())
      .def(self <= uint16_t())
      .def(self > uint16_t())
      .def(self < uint16_t())
      .def(self >= Key_())
      .def(self <= Key_())
      .def(self > Key_())
      .def(self < Key_())
     ;
      
     def("keyToName", &keyToName,
         "Maps a key to its associated key name.\n\n"
         "Args:\n"
         "   key (Key): The key to map.\n\n"
         "Returns:\n"
         "   string: The key name.");
      
      def("keycodeToName", &keycodeToName,
         "Maps a keycode to its associated key name.\n\n"
         "Args:\n"
         "   keycode (int): The keycode to map.\n\n"
         "Returns:\n"
         "   string: The keycode name.");
      
   #define REGISTER_MODIFIER_FUNCTIONS(MOD) \
      def("add"#MOD, &m_##MOD, \
         "Adds modifier \"" #MOD "\" to a key.\n\n" \
         "Returns:\n" \
         "   Key: The key with modifier \"" #MOD "\" enabled.");
      
      FOR_ALL_MODIFIERS(REGISTER_MODIFIER_FUNCTIONS)
      
   #define REGISTER_HELD_MODIFIER_FUNCTIONS(MOD) \
      def("mod"#MOD, &hm_##MOD, \
         "Returns the modifier identifier \"" #MOD "\".\n\n" \
         "Returns:\n" \
         "   int: The key modifier identifier \"" #MOD "\"." \
      );
      
      FOR_ALL_HELD_MODIFIERS(REGISTER_HELD_MODIFIER_FUNCTIONS)
      
   #define EXPORT_KEY_FUNCTIONS(KEY) \
      def("key"#KEY, &k_##KEY, \
         "Returns the key \"" #KEY "\".\n\n" \
         "Returns:\n" \
         "   Key: The key \"" #KEY "\"." \
      );
      
      FOR_ALL_KEYS(EXPORT_KEY_FUNCTIONS)
      
   def("modifierToName", &modifierToName,
         "Maps a modifier ID to its associated name.\n\n"
         "Args:\n"
         "   modifier (int): The modifier ID to map.\n\n"
         "Returns:\n"
         "   string: The modifier name.");
   
   #define EXPORT_METHOD(NAME, DOCSTRING) \
      .def(#NAME, &kaleidoscope::PYTHON::KeyboardReport::NAME, DOCSTRING)
      
   class_<kaleidoscope::PYTHON::KeyboardReport>("KeyboardReport",
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
         isModifierActive,
         "Checks if a modifier is active in the key report.\n\n"
         "Args:\n"
         "   modifier (int): The modifier to check.\n\n"
         "Returns:\n"
         "   boolean: True if the given modifier is active in the key report."
      )
      
      EXPORT_METHOD(
         dump,
         "Dumps the key report to stdout."
      )
   ;
      
   #define EXPORT_STATIC_METHOD(NAME, DOCSTRING) \
      def(#NAME, &kaleidoscope::PYTHON::API::NAME, DOCSTRING);
      
   EXPORT_STATIC_METHOD(
      init,
      "Initializes Kaleidoscope."
   )

   EXPORT_STATIC_METHOD(
      scanCycle,
      "Performs a keyboard scan cycle."
   )
   
   EXPORT_STATIC_METHOD(
      tap,
      "Taps a key at a given position.\n\n"
      "Args:\n"
      "   row (int): The keymap row.\n"
      "   col (int): The keymap column.\n"
   )
   
   EXPORT_STATIC_METHOD(
      getMillis,
      "Returns the current state of the milliseconds timer.\n\n"
      "Returns:\n"
      "   long unsigned: The current state of the milliseconds timer."
   )
   
   EXPORT_STATIC_METHOD(
      setMillis,
      "Sets the current state of the milliseconds timer.\n\n"
      "Args:\n"
      "   millis (long unsigned): The new state of the milliseconds timer."
   )
   
   EXPORT_STATIC_METHOD(
      setKeyboardReportCallback,
      "Allows to set a keyboard report callback.\n\n"
      "Args:\n"
      "   object (python object): A python class object that provides a "
      "processReport(keyboardReport) method that can be passed KeyboardReport class object"
   )
   
   def("getVersionString", &kaleidoscope::PYTHON::getVersionString,
      "Returns the current version of Kaleidoscope-Python.\n\n"
      "Returns:\n"
      "   string: The version string."
   )
   ;
   
   // Cycles are handled on the python side
//    def("currentCycle", &currentCycle);
   
   #define EXPORT_STATIC_KEY_METHOD(NAME, DOCSTRING) \
      def(#NAME, &kaleidoscope::PYTHON::API::NAME, DOCSTRING);
      EXPORT_STATIC_KEY_METHOD(
         keyDown,
         "Registeres a key being pressed at a given position.\n\n"
         "Args:\n"
         "   row (int): The keymap row.\n"
         "   col (int): The keymap column.\n"
      )
         
      EXPORT_STATIC_KEY_METHOD(
         keyUp,
         "Registeres a key being released at a given position.\n\n"
         "Args:\n"
         "   row (int): The keymap row.\n"
         "   col (int): The keymap column.\n"
      )
      
      EXPORT_STATIC_KEY_METHOD(
         clearAllKeys,
         "Releases all keys that are currently pressed."
      )
}
