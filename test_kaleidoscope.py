#!/usr/bin/python

import kaleidoscope

kaleidoscope.API.init()

def keyreport_callback(key_report):
   print "shift set: %d" % key_report.isModifierActive(kaleidoscope.Key.SHIFT_HELD())
   print "key A set: %d" % key_report.isKeyActive(kaleidoscope.Key.Key_A())
   
kaleidoscope.API.setKeyboardReportCallback(keyreport_callback)

kaleidoscope.API.keyDown(2, 1)

kaleidoscope.API.loop()
