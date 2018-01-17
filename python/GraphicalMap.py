# -*- coding: utf-8 -*-
# -*- mode: Python -*-
# Leidokos-Python -- Wraps Kaleidoscope modules' c++
#    code to be available in Python programs.
# Copyright (C) 2017 noseglasses <shinynoseglasses@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import kaleidoscope
from kaleidoscope import *

hidCodeToString = {
   0x04 : u"A", # HID_KEYBOARD_A_AND_A
   0x05 : u"B", # HID_KEYBOARD_B_AND_B
   0x06 : u"C", # HID_KEYBOARD_C_AND_C
   0x07 : u"D", # HID_KEYBOARD_D_AND_D
   0x08 : u"E", # HID_KEYBOARD_E_AND_E
   0x09 : u"F", # HID_KEYBOARD_F_AND_F
   0x0A : u"G", # HID_KEYBOARD_G_AND_G
   0x0B : u"H", # HID_KEYBOARD_H_AND_H
   0x0C : u"I", # HID_KEYBOARD_I_AND_I
   0x0D : u"J", # HID_KEYBOARD_J_AND_J
   0x0E : u"K", # HID_KEYBOARD_K_AND_K
   0x0F : u"L", # HID_KEYBOARD_L_AND_L
   0x10 : u"M", # HID_KEYBOARD_M_AND_M
   0x11 : u"N", # HID_KEYBOARD_N_AND_N
   0x12 : u"O", # HID_KEYBOARD_O_AND_O
   0x13 : u"P", # HID_KEYBOARD_P_AND_P
   0x14 : u"Q", # HID_KEYBOARD_Q_AND_Q
   0x15 : u"R", # HID_KEYBOARD_R_AND_R
   0x16 : u"S", # HID_KEYBOARD_S_AND_S
   0x17 : u"T", # HID_KEYBOARD_T_AND_T
   0x18 : u"U", # HID_KEYBOARD_U_AND_U
   0x19 : u"V", # HID_KEYBOARD_V_AND_V
   0x1A : u"W", # HID_KEYBOARD_W_AND_W
   0x1B : u"X", # HID_KEYBOARD_X_AND_X
   0x1C : u"Y", # HID_KEYBOARD_Y_AND_Y
   0x1D : u"Z", # HID_KEYBOARD_Z_AND_Z
   0x1E : u"1 !", # HID_KEYBOARD_1_AND_EXCLAMATION_POINT
   0x1F : u"2 @", # HID_KEYBOARD_2_AND_AT
   0x20 : u"3 #", # HID_KEYBOARD_3_AND_POUND
   0x21 : u"4 $", # HID_KEYBOARD_4_AND_DOLLAR
   0x22 : u"5 %", # HID_KEYBOARD_5_AND_PERCENT
   0x23 : u"6 ^", # HID_KEYBOARD_6_AND_CARAT
   0x24 : u"7 &", # HID_KEYBOARD_7_AND_AMPERSAND
   0x25 : u"8 *", # HID_KEYBOARD_8_AND_ASTERISK
   0x26 : u"9 (", # HID_KEYBOARD_9_AND_LEFT_PAREN
   0x27 : u"0 )", # HID_KEYBOARD_0_AND_RIGHT_PAREN
   0x28 : "Entr", # HID_KEYBOARD_ENTER	0x28	 // (MARKED AS ENTER_SLASH_RETURN)
   0x29 : u"Esc", # HID_KEYBOARD_ESCAPE
   0x2A : u"Del", # HID_KEYBOARD_DELETE	0x2A	// (BACKSPACE)
   0x2B : u"Tab", # HID_KEYBOARD_TAB
   0x2C : u'Spce', # HID_KEYBOARD_SPACEBAR
   0x2D : u"- _", # HID_KEYBOARD_MINUS_AND_UNDERSCORE	0x2D	 // (UNDERSCORE)
   0x2E : u"= +", # HID_KEYBOARD_EQUALS_AND_PLUS
   0x2F : u"[ {", # HID_KEYBOARD_LEFT_BRACKET_AND_LEFT_CURLY_BRACE
   0x30 : u"] }", # HID_KEYBOARD_RIGHT_BRACKET_AND_RIGHT_CURLY_BRACE
   0x31 : u"\ |", # HID_KEYBOARD_BACKSLASH_AND_PIPE
   0x32 : u"~", # HID_KEYBOARD_NON_US_POUND_AND_TILDE
   0x33 : u"; :", # HID_KEYBOARD_SEMICOLON_AND_COLON
   0x34 : u"\' \"", # HID_KEYBOARD_QUOTE_AND_DOUBLEQUOTE
   0x35 : u"` ~", # HID_KEYBOARD_GRAVE_ACCENT_AND_TILDE
   0x36 : u", <", # HID_KEYBOARD_COMMA_AND_LESS_THAN
   0x37 : u". >", # HID_KEYBOARD_PERIOD_AND_GREATER_THAN
   0x38 : u"/ ?", # HID_KEYBOARD_SLASH_AND_QUESTION_MARK
   0x39 : u"C.L.", # HID_KEYBOARD_CAPS_LOCK
   0x3A : u"F1", # HID_KEYBOARD_F1
   0x3B : u"F2", # HID_KEYBOARD_F2
   0x3C : u"F3", # HID_KEYBOARD_F3
   0x3D : u"F4", # HID_KEYBOARD_F4
   0x3E : u"F5", # HID_KEYBOARD_F5
   0x3F : u"F6", # HID_KEYBOARD_F6
   0x40 : u"F7", # HID_KEYBOARD_F7
   0x41 : u"F8", # HID_KEYBOARD_F8
   0x42 : u"F9", # HID_KEYBOARD_F9
   0x43 : u"F10", # HID_KEYBOARD_F10
   0x44 : u"F11", # HID_KEYBOARD_F11
   0x45 : u"F12", # HID_KEYBOARD_F12
   0x46 : u"PRTS", # HID_KEYBOARD_PRINTSCREEN
   0x47 : u"ScLk", # HID_KEYBOARD_SCROLL_LOCK
   0x48 : u"Pse", # HID_KEYBOARD_PAUSE
   0x49 : u"Isrt", # HID_KEYBOARD_INSERT
   0x4A : u"Home", # HID_KEYBOARD_HOME
   0x4B : u"PgUp", # HID_KEYBOARD_PAGE_UP
   0x4C : u"Del", # HID_KEYBOARD_DELETE_FORWARD
   0x4D : u"End", # HID_KEYBOARD_END
   0x4E : u"PgDn", # HID_KEYBOARD_PAGE_DOWN
   0x4F : u"→", # HID_KEYBOARD_RIGHT_ARROW
   0x50 : u"←", # HID_KEYBOARD_LEFT_ARROW
   0x51 : u"↓", # HID_KEYBOARD_DOWN_ARROW
   0x52 : u"↑", # HID_KEYBOARD_UP_ARROW
   0x53 : u"NlCl", # HID_KEYPAD_NUM_LOCK_AND_CLEAR
   0x54 : u"/", # HID_KEYPAD_DIVIDE
   0x55 : u"*", # HID_KEYPAD_MULTIPLY
   0x56 : u"-", # HID_KEYPAD_SUBTRACT
   0x57 : u"+", # HID_KEYPAD_ADD
   0x58 : u"Entr", # HID_KEYPAD_ENTER
   0x59 : u"1 Ed", # HID_KEYPAD_1_AND_END
   0x5A : u"2 ↓", # HID_KEYPAD_2_AND_DOWN_ARROW
   0x5B : u"3 PD", # HID_KEYPAD_3_AND_PAGE_DOWN
   0x5C : u"4 ←", # HID_KEYPAD_4_AND_LEFT_ARROW
   0x5D : u"5", # HID_KEYPAD_5
   0x5E : u"6 →", # HID_KEYPAD_6_AND_RIGHT_ARROW
   0x5F : u"7 Hm", # HID_KEYPAD_7_AND_HOME
   0x60 : u"8 ↑", # HID_KEYPAD_8_AND_UP_ARROW
   0x61 : u"9 PU", # HID_KEYPAD_9_AND_PAGE_UP
   0x62 : u"0 IN", # HID_KEYPAD_0_AND_INSERT
   0x63 : u". DL", # HID_KEYPAD_PERIOD_AND_DELETE
   0x64 : u"\ |", # HID_KEYBOARD_NON_US_BACKSLASH_AND_PIPE
   #0x65 : # HID_KEYBOARD_APPLICATION
   #0x66 : # HID_KEYBOARD_POWER
   0x67 : u"=", # HID_KEYPAD_EQUALS
   0x68 : u"F13", # HID_KEYBOARD_F13
   0x69 : u"F14", # HID_KEYBOARD_F14
   0x6A : u"F15", # HID_KEYBOARD_F15
   0x6B : u"F16", # HID_KEYBOARD_F16
   0x6C : u"F17", # HID_KEYBOARD_F17
   0x6D : u"F18", # HID_KEYBOARD_F18
   0x6E : u"F19", # HID_KEYBOARD_F19
   0x6F : u"F20", # HID_KEYBOARD_F20
   0x70 : u"F21", # HID_KEYBOARD_F21
   0x71 : u"F22", # HID_KEYBOARD_F22
   0x72 : u"F23", # HID_KEYBOARD_F23
   0x73 : u"F24", # HID_KEYBOARD_F24
   #0x74 :  , # HID_KEYBOARD_EXECUTE
   #0x75 :  , # HID_KEYBOARD_HELP
   #0x76 :  , # HID_KEYBOARD_MENU
   #0x77 :  , # HID_KEYBOARD_SELECT
   #0x78 :  , # HID_KEYBOARD_STOP
   #0x79 :  , # HID_KEYBOARD_AGAIN
   #0x7A :  , # HID_KEYBOARD_UNDO
   #0x7B :  , # HID_KEYBOARD_CUT
   #0x7C :  , # HID_KEYBOARD_COPY
   #0x7D :  , # HID_KEYBOARD_PASTE
   #0x7E :  , # HID_KEYBOARD_FIND
   #0x7F :  , # HID_KEYBOARD_MUTE
   #0x80 :  , # HID_KEYBOARD_VOLUME_UP
   #0x81 :  , # HID_KEYBOARD_VOLUME_DOWN
   #0x82 :  , # HID_KEYBOARD_LOCKING_CAPS_LOCK
   #0x83 :  , # HID_KEYBOARD_LOCKING_NUM_LOCK
   #0x84 :  , # HID_KEYBOARD_LOCKING_SCROLL_LOCK
   0x85 : u",", # HID_KEYPAD_COMMA
   0x86 : u"=", # HID_KEYPAD_EQUAL_SIGN
}

def _getColorEscSeq(row, col):  
   
   #red = random.randint(0, 255)
   #green = random.randint(0, 255)
   #blue = random.randint(0, 255)
   
   color = LEDs.getCrgbAt(row, col)
   
   red = color.getRed()
   green = color.getGreen()
   blue = color.getBlue()
   
   col_norm = red*red + green*green + blue*blue
   
   # Have black text on dark background color and wi
   if col_norm > 49152:
      forground_color = "0"
   else:
      forground_color = "15"
      
   return "\x1b[48;2;{red};{green};{blue}m" \
            "\x1b[38;5;{forground_color}m" \
      .format(red = red, green = green, blue = blue,
               forground_color = forground_color)

def _generateKeyString(row, col):
   
   layer = kaleidoscope.Layer.lookupActiveLayer(row, col)
   key = kaleidoscope.Layer.lookupOnActiveLayer(row, col)
   
   verboseDescription = True
   if key.getFlags() == KEY_FLAGS():
      
      # Normal key
      #
      # TODO: Map the keycode to a (unicode) string that matches the key
      # 
      keyCode = key.getKeyCode()
      if keyCode in hidCodeToString.keys():
         keyString = hidCodeToString[keyCode]
         verboseDescription = False
   
   if verboseDescription:
      keyString = kaleidoscope.getKeyDescription(layer, row, col)
   
   #if len(keyString) < 4: 
      #return keyString
   
   #return keyString[:4]
   
   colString = _getColorEscSeq(row, col)
   
   # Limit the key caption to the with of the cell
   #
   #actual_keystring = '{:4.4}'.format(keyString)
   
   return (colString, keyString)
   
   #return '{0}{1}{2}'.format(col_string, actual_keystring, neutral_string)
   
def graphicalMap(out, hardware):
   
   rows = kaleidoscope.matrixRows()
   cols = kaleidoscope.matrixCols()
   
   keyStrings = []
   
   # Escape sequences to restore default foreground and 
   # background colors
   #
   neutralString = "\x1b[39;49m"  
   
   keyStringMap = {}
   keyStringIndex = 1
   
   for row in range(rows):
      for col in range(cols):
         (colString, keyString) = _generateKeyString(row, col)
         
         if len(keyString) > 4:
            if not keyString in keyStringMap.keys():
               keyStringMap[keyString] = keyStringIndex
               curKeyStringIndex = keyStringIndex
               keyStringIndex += 1
            else:
               curKeyStringIndex = keyStringMap[keyString]
               
            keyString = "*%3.3d" % curKeyStringIndex
         else:
            keyString = '{:4.4}'.format(keyString)
            
         keyStrings.append("{0}{1}{2}".format(
            colString, keyString, neutralString))
   
   hardware.printKeymap(out, keyStrings)

   for keyString in sorted(keyStringMap, key=keyStringMap.get):
      out.write("%3.3d %s\n" % (keyStringMap[keyString], keyString))
