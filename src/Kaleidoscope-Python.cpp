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
#include "KeyboardReport.h"

#include "virtual_io.h"
#include "Kaleidoscope-Hardware-Virtual.h"

#include <string.h>
#include <iostream>
#include <sstream>

namespace kaleidoscope {
namespace python {
   
class API
{
   public:
      
      static void init();
      
      static void scanCycle();
      
      static void tap(byte row, byte col);
      static void keyDown(byte row, byte col);
      static void keyUp(byte row, byte col);
      static void clearAllKeys();
      
      static void setMillis(unsigned long millis);
      static unsigned long getMillis();
      
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
      
      static unsigned long millis_;
};

} // namespace python
} // namespace kaleidoscope

// Also defined by Kaleidoscope-Hardware-Virtual
//
void initVariant() __attribute__((weak));
void setup(void);

unsigned long millis(void) {
   return kaleidoscope::python::API::getMillis();
}

extern Virtual KeyboardHardware;

namespace kaleidoscope {
namespace python {

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

// Generating KaleidoscopePluginRegistrationCallbacks as a static
// function scope variable avoids the "static initialization order fiasco".
//
PluginRegistrationCallbacks &pluginRegistrationCallbacks() {
   static PluginRegistrationCallbacks cb;
   return cb;
}

} // namespace python
} // namespace kaleidoscope

BOOST_PYTHON_MODULE(KALEIDOSCOPE_PYTHON_PACKAGE_NAME)
{
   // specify that this module is actually a package
   //
   boost::python::object package = boost::python::scope();
   package.attr("__path__") = STRINGIZE(KALEIDOSCOPE_PYTHON_PACKAGE_NAME);
   
   auto &registrationCallbacks 
      = kaleidoscope::python::pluginRegistrationCallbacks();
   
   for(auto &cb: registrationCallbacks) {
      cb();
   }
      
   #define EXPORT_STATIC_METHOD(NAME, DOCSTRING) \
      boost::python::def(#NAME, &kaleidoscope::python::API::NAME, DOCSTRING);
      
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
   
   boost::python::def("millis", &millis, 
      "Returns the current state of the milliseconds timer.\n\n"
      "Returns:\n"
      "   long unsigned: The current state of the milliseconds timer."
   );
   
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
   
   boost::python::def("getVersionString", &kaleidoscope::python::getVersionString,
      "Returns the current version of Kaleidoscope-Python.\n\n"
      "Returns:\n"
      "   string: The version string."
   )
   ;
   
   // Cycles are handled on the python side
//    def("currentCycle", &currentCycle);
   
   #define EXPORT_STATIC_KEY_METHOD(NAME, DOCSTRING) \
      boost::python::def(#NAME, &kaleidoscope::python::API::NAME, DOCSTRING);
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
