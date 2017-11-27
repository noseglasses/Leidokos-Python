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

#include <string.h>

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
   
   if(this->keyboardReportCallback_) {
      this->keyboardReportCallback_(this->keyboardReport_);
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
   static Key_ k_##KEY() { return KEY; }

FOR_ALL_KEYS(DEFINE_KEY_FUNCTIONS)

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
      ;
   
   #define EXPORT_METHOD(NAME) \
      .def(#NAME, &kaleidoscope::python_wrapper::KeyboardReport::NAME)
   
   class_<kaleidoscope::python_wrapper::KeyboardReport>("KeyboardReport")
      EXPORT_METHOD(isKeycodeActive)
      EXPORT_METHOD(isKeyActive)
      EXPORT_METHOD(isModifierActive)
   ;
      
   #define EXPORT_STATIC_METHOD(NAME) \
      .def(#NAME, &kaleidoscope::python_wrapper::API::NAME).staticmethod(#NAME)
      
   class_<kaleidoscope::python_wrapper::API>("API")
      EXPORT_STATIC_METHOD(init)
      EXPORT_STATIC_METHOD(loop)
      EXPORT_STATIC_METHOD(tap)
      EXPORT_STATIC_METHOD(keyDown)
      EXPORT_STATIC_METHOD(keyUp)
      EXPORT_STATIC_METHOD(clearAllKeys)
      EXPORT_STATIC_METHOD(setKeyboardReportCallback)
   ;
}
