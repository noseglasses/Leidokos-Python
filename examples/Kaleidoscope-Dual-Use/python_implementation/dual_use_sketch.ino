// -*- mode: c++ -*-
// Leidokos-Python -- Wraps Kaleidoscope modules' c++
//    code to be available in Python programs.
// Copyright (C) 2017 noseglasses <shinynoseglasses@gmail.com>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#ifndef BUILD_INFORMATION
#define BUILD_INFORMATION "locally built"
#endif

// The Kaleidoscope core
#include "Kaleidoscope.h"

// Even though we do not access dual use in this sketch, we need 
// the macro CTL_T to be defined.
//
#include "Kaleidoscope-DualUse.h"

enum { QWERTY }; // layers

/* This comment temporarily turns off astyle's indent enforcement
 *   so we can make the keymaps actually resemble the physical key layout better
 */
// *INDENT-OFF*

const Key keymaps[][ROWS][COLS] PROGMEM = {

  [QWERTY] = KEYMAP_STACKED
  (___,          CTL_T(1), Key_2, Key_3, Key_4, Key_5, ___,
   Key_Backtick, Key_Q, Key_W, Key_E, Key_R, Key_T, Key_Tab,
   Key_PageUp,   Key_A, Key_S, Key_D, Key_F, Key_G,
   Key_PageDown, Key_Z, Key_X, Key_C, Key_V, Key_B, Key_Escape,
   Key_LeftControl, Key_Backspace, Key_LeftGui, Key_LeftShift,
   ___,

   ___,           Key_6, Key_7, Key_8,     Key_9,         Key_0,         ___,
   Key_Enter,     Key_Y, Key_U, Key_I,     Key_O,         Key_P,         Key_Equals,
                  Key_H, Key_J, Key_K,     Key_L,         Key_Semicolon, Key_Quote,
   Key_RightAlt,  Key_N, Key_M, Key_Comma, Key_Period,    Key_Slash,     Key_Minus,
   Key_RightShift, Key_LeftAlt, Key_Spacebar, Key_RightControl,
   ___)
};

/* Re-enable astyle's indent enforcement */
// *INDENT-ON*

void setup() {
  Kaleidoscope.setup();
}

void loop() {
  Kaleidoscope.loop();
}
