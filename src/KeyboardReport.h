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

#ifndef KP_KEYBOARD_REPORT_HPP
#define KP_KEYBOARD_REPORT_HPP

#include "VirtualHID/Keyboard.h"

#include <boost/python.hpp>

namespace kaleidoscope {
namespace python {
   
class KeyboardReport {
   
   public:
      
      bool isKeycodeActive(uint8_t k) const;
      bool isKeyActive(const Key_ &k) const;
      boost::python::list getActiveKeycodes() const;
      
      bool isModifierKeycodeActive(uint8_t modifier) const;
      bool isModifierActive(const Key &key) const;
      
      bool isAnyModifierActive() const;
      bool isAnyKeyActive() const;
      
      boost::python::list getActiveModifiers() const;
      
      bool isEmpty() const;
      
      std::string dump() const;
      
      void setReportData(const HID_KeyboardReport_Data_t &reportData);
      
   private:
   
      HID_KeyboardReport_Data_t reportData_;
};

} // namespace python
} // namespace kaleidoscope

#endif
