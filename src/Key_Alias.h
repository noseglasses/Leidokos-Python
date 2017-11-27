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

#ifndef KALEIDOSCOPE_PYTHON_WRAPPER__KEY_ALIAS_H
#define KALEIDOSCOPE_PYTHON_WRAPPER__KEY_ALIAS_H
   
#define FOR_ALL_KEYS(FUNC) \
   FUNC(Key_NoEvent) \
   FUNC(Key_ErrorRollover) \
   FUNC(Key_PostFail) \
   FUNC(Key_ErrorUndefined) \
   FUNC(Key_A) \
   FUNC(Key_B) \
   FUNC(Key_C) \
   FUNC(Key_D) \
   FUNC(Key_E) \
   FUNC(Key_F) \
   FUNC(Key_G) \
   FUNC(Key_H) \
   FUNC(Key_I) \
   FUNC(Key_J) \
   FUNC(Key_K) \
   FUNC(Key_L) \
   FUNC(Key_M) \
   FUNC(Key_N) \
   FUNC(Key_O) \
   FUNC(Key_P) \
   FUNC(Key_Q) \
   FUNC(Key_R) \
   FUNC(Key_S) \
   FUNC(Key_T) \
   FUNC(Key_U) \
   FUNC(Key_V) \
   FUNC(Key_W) \
   FUNC(Key_X) \
   FUNC(Key_Y) \
   FUNC(Key_Z) \
   FUNC(Key_1) \
   FUNC(Key_2) \
   FUNC(Key_3) \
   FUNC(Key_4) \
   FUNC(Key_5) \
   FUNC(Key_6) \
   FUNC(Key_7) \
   FUNC(Key_8) \
   FUNC(Key_9) \
   FUNC(Key_0) \
   FUNC(Key_Enter) \
   FUNC(Key_Escape) \
   FUNC(Key_Backspace) \
   FUNC(Key_Tab) \
   FUNC(Key_Spacebar) \
   FUNC(Key_Minus) \
   FUNC(Key_Equals) \
   FUNC(Key_LeftBracket) \
   FUNC(Key_RightBracket) \
   FUNC(Key_Backslash) \
   FUNC(Key_NonUsPound) \
   FUNC(Key_Semicolon) \
   FUNC(Key_Quote) \
   FUNC(Key_Backtick) \
   FUNC(Key_Comma) \
   FUNC(Key_Period) \
   FUNC(Key_Slash) \
   FUNC(Key_CapsLock) \
   FUNC(Key_F1) \
   FUNC(Key_F2) \
   FUNC(Key_F3) \
   FUNC(Key_F4) \
   FUNC(Key_F5) \
   FUNC(Key_F6) \
   FUNC(Key_F7) \
   FUNC(Key_F8) \
   FUNC(Key_F9) \
   FUNC(Key_F10) \
   FUNC(Key_F11) \
   FUNC(Key_F12) \
   FUNC(Key_PrintScreen) \
   FUNC(Key_ScrollLock) \
   FUNC(Key_Pause) \
   FUNC(Key_Insert) \
   FUNC(Key_Home) \
   FUNC(Key_PageUp) \
   FUNC(Key_Delete) \
   FUNC(Key_End) \
   FUNC(Key_PageDown) \
   FUNC(Key_RightArrow) \
   FUNC(Key_LeftArrow) \
   FUNC(Key_DownArrow) \
   FUNC(Key_UpArrow) \
   FUNC(Key_KeypadNumLock) \
   FUNC(Key_KeypadDivide) \
   FUNC(Key_KeypadMultiply) \
   FUNC(Key_KeypadSubtract) \
   FUNC(Key_KeypadAdd) \
   FUNC(Key_KeypadEnter) \
   FUNC(Key_Keypad1) \
   FUNC(Key_Keypad2) \
   FUNC(Key_Keypad3) \
   FUNC(Key_Keypad4) \
   FUNC(Key_Keypad5) \
   FUNC(Key_Keypad6) \
   FUNC(Key_Keypad7) \
   FUNC(Key_Keypad8) \
   FUNC(Key_Keypad9) \
   FUNC(Key_Keypad0) \
   FUNC(Key_KeypadDot) \
   FUNC(Key_NonUsBackslashAndPipe) \
   FUNC(Key_PcApplication) \
   FUNC(Key_Power) \
   FUNC(Key_KeypadEquals) \
   FUNC(Key_F13) \
   FUNC(Key_F14) \
   FUNC(Key_F15) \
   FUNC(Key_F16) \
   FUNC(Key_F17) \
   FUNC(Key_F18) \
   FUNC(Key_F19) \
   FUNC(Key_F20) \
   FUNC(Key_F21) \
   FUNC(Key_F22) \
   FUNC(Key_F23) \
   FUNC(Key_F24) \
   FUNC(Key_Execute) \
   FUNC(Key_Help) \
   FUNC(Key_Menu) \
   FUNC(Key_Select) \
   FUNC(Key_Stop) \
   FUNC(Key_Again) \
   FUNC(Key_Undo) \
   FUNC(Key_Cut) \
   FUNC(Key_Copy) \
   FUNC(Key_Paste) \
   FUNC(Key_Find) \
   FUNC(Key_Mute) \
   FUNC(Key_VolumeUp) \
   FUNC(Key_VolumeDown) \
   FUNC(Key_LockingCapsLock) \
   FUNC(Key_LockingNumLock) \
   FUNC(Key_LockingScrollLock) \
   FUNC(Key_KeypadComma) \
   FUNC(Key_KeypadEqualSign) \
   FUNC(Key_International1) \
   FUNC(Key_International2) \
   FUNC(Key_International3) \
   FUNC(Key_International4) \
   FUNC(Key_International5) \
   FUNC(Key_International6) \
   FUNC(Key_International7) \
   FUNC(Key_International8) \
   FUNC(Key_International9) \
   FUNC(Key_Lang1) \
   FUNC(Key_Lang2) \
   FUNC(Key_Lang3) \
   FUNC(Key_Lang4) \
   FUNC(Key_Lang5) \
   FUNC(Key_Lang6) \
   FUNC(Key_Lang7) \
   FUNC(Key_Lang8) \
   FUNC(Key_Lang9) \
   FUNC(Key_AlternateErase) \
   FUNC(Key_Sysreq) \
   FUNC(Key_Cancel) \
   FUNC(Key_Clear) \
   FUNC(Key_Prior) \
   FUNC(Key_Return) \
   FUNC(Key_Separator) \
   FUNC(Key_Out) \
   FUNC(Key_Oper) \
   FUNC(Key_ClearSlashAgain) \
   FUNC(Key_CrselSlashProps) \
   FUNC(Key_Exsel) \
   FUNC(Key_Keypad00) \
   FUNC(Key_Keypad000) \
   FUNC(Key_ThousandsSeparator) \
   FUNC(Key_DecimalSeparator) \
   FUNC(Key_CurrencyUnit) \
   FUNC(Key_CurrencySubunit) \
   FUNC(Key_KeypadLeftParen) \
   FUNC(Key_KeypadRightParen) \
   FUNC(Key_KeypadLeftCurlyBrace) \
   FUNC(Key_KeypadRightCurlyBrace) \
   FUNC(Key_KeypadTab) \
   FUNC(Key_KeypadBackspace) \
   FUNC(Key_KeypadA) \
   FUNC(Key_KeypadB) \
   FUNC(Key_KeypadC) \
   FUNC(Key_KeypadD) \
   FUNC(Key_KeypadE) \
   FUNC(Key_KeypadF) \
   FUNC(Key_KeypadXor) \
   FUNC(Key_KeypadCarat) \
   FUNC(Key_KeypadPercent) \
   FUNC(Key_KeypadLessThan) \
   FUNC(Key_KeypadGreaterThan) \
   FUNC(Key_KeypadAmpersand) \
   FUNC(Key_KeypadDoubleampersand) \
   FUNC(Key_KeypadPipe) \
   FUNC(Key_KeypadDoublepipe) \
   FUNC(Key_KeypadColon) \
   FUNC(Key_KeypadPoundSign) \
   FUNC(Key_KeypadSpace) \
   FUNC(Key_KeypadAtSign) \
   FUNC(Key_KeypadExclamationPoint) \
   FUNC(Key_KeypadMemoryStore) \
   FUNC(Key_KeypadMemoryRecall) \
   FUNC(Key_KeypadMemoryClear) \
   FUNC(Key_KeypadMemoryAdd) \
   FUNC(Key_KeypadMemorySubtract) \
   FUNC(Key_KeypadMemoryMultiply) \
   FUNC(Key_KeypadMemoryDivide) \
   FUNC(Key_KeypadPlusSlashMinus) \
   FUNC(Key_KeypadClear) \
   FUNC(Key_KeypadClearEntry) \
   FUNC(Key_KeypadBinary) \
   FUNC(Key_KeypadOctal) \
   FUNC(Key_KeypadDecimal) \
   FUNC(Key_KeypadHexadecimal) \
   FUNC(Key_LeftControl) \
   FUNC(Key_LeftShift) \
   FUNC(Key_LeftAlt) \
   FUNC(Key_LeftGui) \
   FUNC(Key_RightControl) \
   FUNC(Key_RightShift) \
   FUNC(Key_RightAlt) \
   FUNC(Key_RightGui) \
   \
   FUNC(Key_Keymap0) \
   FUNC(Key_Keymap1) \
   FUNC(Key_Keymap2) \
   FUNC(Key_Keymap3) \
   FUNC(Key_Keymap4) \
   FUNC(Key_Keymap5) \
   FUNC(Key_Keymap0_Momentary) \
   FUNC(Key_Keymap1_Momentary) \
   FUNC(Key_Keymap2_Momentary) \
   FUNC(Key_Keymap3_Momentary) \
   FUNC(Key_Keymap4_Momentary) \
   FUNC(Key_Keymap5_Momentary) \
   \
   FUNC(Key_KeymapNext_Momentary) \
   FUNC(Key_KeymapPrevious_Momentary) \
   \
   FUNC(Key_NoKey) \
   FUNC(Key_skip) \
   FUNC(Key_Transparent)
   
#define FOR_ALL_MODIFIERS(FUNC) \
   FUNC(LCTRL) \
   FUNC(LALT) \
   FUNC(RALT) \
   FUNC(LSHIFT) \
   FUNC(LGUI)
   
#define FOR_ALL_HELD_MODIFIERS(FUNC) \
   FUNC(KEY_FLAGS) \
   FUNC(CTRL_HELD) \
   FUNC(LALT_HELD) \
   FUNC(RALT_HELD) \
   FUNC(SHIFT_HELD) \
   FUNC(GUI_HELD) \
   FUNC(SYNTHETIC) \
   FUNC(RESERVED)
   
#endif
