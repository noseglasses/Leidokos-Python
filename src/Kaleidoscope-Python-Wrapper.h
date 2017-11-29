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

#ifndef KALEIDOSCOPE_PYTHON_WRAPPER_H
#define KALEIDOSCOPE_PYTHON_WRAPPER_H

#include <boost/python.hpp>

#include "Kaleidoscope-Hardware-Virtual.h"
#include "Kaleidoscope-Python-Wrapper.h"
#include "VirtualHID/Keyboard.h"

#include "key_defs.h"

#include <string>

namespace kaleidoscope {
namespace python_wrapper {
   
class KeyboardReport {
   
   public:
      
      bool isKeycodeActive(uint8_t k) const;
      bool isKeyActive(const Key_ &k) const;
      bool isModifierActive(uint8_t modifier) const;
      
      std::string dump() const;
      
      void setReportData(const HID_KeyboardReport_Data_t &reportData);
      
   private:
   
      HID_KeyboardReport_Data_t reportData_;
};

class API
{
   public:
      
      static void init();
      
      static void loop();
      
      static void tap(byte row, byte col);
      static void keyDown(byte row, byte col);
      static void keyUp(byte row, byte col);
      static void clearAllKeys();
      
      static void setKeyboardReportCallback(boost::python::object func);
      
   private:

      class KeyboardReportConsumer : public KeyboardReportConsumer_
      {
         public:
            
            friend class API;
            
            virtual void processKeyboardReport(
                           const HID_KeyboardReport_Data_t &reportData) override;
                           
         private:
            
            boost::python::object keyboardReportCallback_;
            
            KeyboardReport keyboardReport_;
      };
      
      static KeyboardReportConsumer keyboardReportConsumer_;
};

} // namespace python_wrapper
} // namespace kaleidoscope

#endif
