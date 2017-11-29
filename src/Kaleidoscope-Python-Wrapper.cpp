/* -*- mode: c++ -*-
 * Kaleidoscope-Python-Wrapper -- Wraps Kaleidoscope modules' c++
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

#include "Kaleidoscope-Python-Wrapper.h"
#include "Key_Alias.h"

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

extern Virtual KeyboardHardware;

namespace kaleidoscope {
namespace python_wrapper {
   
API::KeyboardReportConsumer API::keyboardReportConsumer_;
   
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
      ::loop()
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

} // namespace python_wrapper
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

BOOST_PYTHON_MODULE(kaleidoscope)
{
   #define EXPORT_LAYER_STATIC_METHOD(NAME) \
      .def(#NAME, &Layer_::NAME).staticmethod(#NAME)
      
   class_<Layer_>("Layer")
      EXPORT_LAYER_STATIC_METHOD(lookup)
      EXPORT_LAYER_STATIC_METHOD(lookupOnActiveLayer)
      EXPORT_LAYER_STATIC_METHOD(on)
      EXPORT_LAYER_STATIC_METHOD(off)
      EXPORT_LAYER_STATIC_METHOD(move)
      EXPORT_LAYER_STATIC_METHOD(top)
      EXPORT_LAYER_STATIC_METHOD(next)
      EXPORT_LAYER_STATIC_METHOD(previous)
      EXPORT_LAYER_STATIC_METHOD(isOn)
      EXPORT_LAYER_STATIC_METHOD(getLayerState)
      EXPORT_LAYER_STATIC_METHOD(eventHandler)
      EXPORT_LAYER_STATIC_METHOD(getKeyFromPROGMEM)
      EXPORT_LAYER_STATIC_METHOD(updateLiveCompositeKeymap)
      EXPORT_LAYER_STATIC_METHOD(updateActiveLayers)
      
      // As there are two overloaded versions of 
      // defaultLayer that are actually a getter and a setter, we have 
      // to point the compiler to the different versions of the functions
      // by casting to the different function pointer types
      //
      .def("getDefaultLayer", static_cast< 
            uint8_t(*)()
         >(&Layer_::defaultLayer)
      ).staticmethod("getDefaultLayer")
      .def("setDefaultLayer", static_cast< 
            void(*)(uint8_t)
         >(&Layer_::defaultLayer)
      ).staticmethod("setDefaultLayer")
    ;
    
   class_<Key_>("Key")
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
      
   #define REGISTER_MODIFIER_FUNCTIONS(MOD) \
      .def(#MOD, &m_##MOD).staticmethod(#MOD)
      
      FOR_ALL_MODIFIERS(REGISTER_MODIFIER_FUNCTIONS)
      
   #define REGISTER_HELD_MODIFIER_FUNCTIONS(MOD) \
      .def(#MOD, &hm_##MOD).staticmethod(#MOD)
      
      FOR_ALL_HELD_MODIFIERS(REGISTER_HELD_MODIFIER_FUNCTIONS)
      
   #define EXPORT_KEY_FUNCTIONS(KEY) \
      .def(#KEY, &k_##KEY).staticmethod(#KEY)
      
      FOR_ALL_KEYS(EXPORT_KEY_FUNCTIONS)
   
      .def("keyToName", &keyToName).staticmethod("keyToName")
      .def("keycodeToName", &keycodeToName).staticmethod("keycodeToName");
      
   class_<Key_>("Modifier")
      .def("toName", &modifierToName).staticmethod("toName");
   
   #define EXPORT_METHOD(NAME) \
      .def(#NAME, &kaleidoscope::python_wrapper::KeyboardReport::NAME)
      
   class_<kaleidoscope::python_wrapper::KeyboardReport>("KeyboardReport")
      EXPORT_METHOD(isKeycodeActive)
      EXPORT_METHOD(isKeyActive)
      EXPORT_METHOD(isModifierActive)
      EXPORT_METHOD(dump)
   ;
      
   #define EXPORT_STATIC_METHOD(NAME) \
      def(#NAME, &kaleidoscope::python_wrapper::API::NAME);
      
   EXPORT_STATIC_METHOD(init)
   EXPORT_STATIC_METHOD(loop)
   EXPORT_STATIC_METHOD(tap)
   EXPORT_STATIC_METHOD(setKeyboardReportCallback)
   
   // Cycles are handled on the python side
//    def("currentCycle", &currentCycle);
   
   #define EXPORT_STATIC_KEY_METHOD(NAME) \
      def(#NAME, &kaleidoscope::python_wrapper::API::NAME);
      EXPORT_STATIC_KEY_METHOD(keyDown)
      EXPORT_STATIC_KEY_METHOD(keyUp)
      EXPORT_STATIC_KEY_METHOD(clearAllKeys)
}
