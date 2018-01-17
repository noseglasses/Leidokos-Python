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

class Hardware(object):
   
   def printKeymap(self, out, keyStrings):
      
      (r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6, r0c7, r0c8, r0c9, r0c10, r0c11, r0c12, r0c13, r0c14, r0c15, \
       r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c6, r1c7, r1c8, r1c9, r1c10, r1c11, r1c12, r1c13, r1c14, r1c15, \
       r2c0, r2c1, r2c2, r2c3, r2c4, r2c5, r2c6, r2c7, r2c8, r2c9, r2c10, r2c11, r2c12, r2c13, r2c14, r2c15, \
       r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r3c6, r3c7, r3c8, r3c9, r3c10, r3c11, r3c12, r3c13, r3c14, r3c15) = \
      tuple(keyStrings)
      
      out.write(u"┏━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓        ┏━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┳━━━━┓\n")
      out.write(u"┃{0}┃{1}┃{2}┃{3}┃{4}┃{5}┃{6}┃        ┃{7}┃{8}┃{9}┃{10}┃{11}┃{12}┃{13}┃\n".format(r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6,        r0c9,  r0c10, r0c11, r0c12, r0c13, r0c14, r0c15))
      out.write(u"┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫    ┃        ┃    ┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫\n")
      out.write(u"┃{0}┃{1}┃{2}┃{3}┃{4}┃{5}┣━━━━┫        ┣━━━━┫{6}┃{7}┃{8}┃{9}┃{10}┃{11}┃\n".format(r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c10, r1c11, r1c12, r1c13, r1c14, r1c15))
      out.write(u"┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫    ┃        ┃    ┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫\n")
      out.write(u"┃{0}┃{1}┃{2}┃{3}┃{4}┃{5}┃{6}┃        ┃{7}┃{8}┃{9}┃{10}┃{11}┃{12}┃{13}┃\n".format(r2c0, r2c1, r2c2, r2c3, r2c4, r2c5, r1c6, r1c9, r2c10, r2c11, r2c12, r2c13, r2c14, r2c15))
      out.write(u"┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫        ┣━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━╋━━━━┫\n")
      out.write(u"┃{0}┃{1}┃{2}┃{3}┃{4}┃{5}┃{6}┃        ┃{7}┃{8}┃{9}┃{10}┃{11}┃{12}┃{13}┃\n".format(r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r2c6,        r2c9,  r3c10, r3c11, r3c12, r3c13, r3c14, r3c15))
      out.write(u"┗━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━━━━┛        ┗━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━━━━┻━━━━┛\n")
      out.write(u"                ┏━━━━┓                                    ┏━━━━┓                \n")
      out.write(u"                ┃{0}┣━━━━┓                          ┏━━━━┫{1}┃                \n".format(r0c7, r0c8))
      out.write(u"                ┗━━━━┫{0}┣━━━━┓                ┏━━━━┫{1}┣━━━━┛                \n".format(r1c7, r1c8))
      out.write(u"                     ┗━━━━┫{0}┣━━━━┓      ┏━━━━┫{1}┣━━━━┛                     \n".format(r2c7, r2c8))
      out.write(u"                          ┗━━━━┫{0}┃      ┃{1}┣━━━━┛                          \n".format(r3c7, r3c8))
      out.write(u"                               ┗━━━━┛      ┗━━━━┛                               \n")
      out.write(u"                    ┏━━━━━━┓                        ┏━━━━━━┓                    \n")
      out.write(u"                    ┃ {0} ┃                        ┃ {1} ┃                    \n".format(r3c6, r3c9))
      out.write(u"                    ┗━━━━━━┛                        ┗━━━━━━┛                    \n")
      
      ##define KEYMAP(                                                                                     \
  #r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6,        r0c9,  r0c10, r0c11, r0c12, r0c13, r0c14, r0c15, \
  #r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c6,        r1c9,  r1c10, r1c11, r1c12, r1c13, r1c14, r1c15, \
  #r2c0, r2c1, r2c2, r2c3, r2c4, r2c5,                     r2c10, r2c11, r2c12, r2c13, r2c14, r2c15, \
  #r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r2c6,        r2c9,  r3c10, r3c11, r3c12, r3c13, r3c14, r3c15, \
              #r0c7, r1c7, r2c7, r3c7,                             r3c8,  r2c8,  r1c8, r0c8,         \
                          #r3c6,                                          r3c9)                      \
  #{                                                                                                 \
    #{r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6, r0c7, r0c8, r0c9, r0c10, r0c11, r0c12, r0c13, r0c14, r0c15}, \
    #{r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c6, r1c7, r1c8, r1c9, r1c10, r1c11, r1c12, r1c13, r1c14, r1c15}, \
    #{r2c0, r2c1, r2c2, r2c3, r2c4, r2c5, r2c6, r2c7, r2c8, r2c9, r2c10, r2c11, r2c12, r2c13, r2c14, r2c15}, \
    #{r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r3c6, r3c7, r3c8, r3c9, r3c10, r3c11, r3c12, r3c13, r3c14, r3c15}, \
  #}

##define KEYMAP_STACKED(                                                 \
               #r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6,                \
               #r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c6,                \
               #r2c0, r2c1, r2c2, r2c3, r2c4, r2c5,                      \
               #r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r2c6,                \
               #r0c7, r1c7, r2c7, r3c7,                                  \
               #r3c6,                                                    \
                                                                        #\
               #r0c9,  r0c10, r0c11, r0c12, r0c13, r0c14, r0c15,         \
               #r1c9,  r1c10, r1c11, r1c12, r1c13, r1c14, r1c15,         \
                      #r2c10, r2c11, r2c12, r2c13, r2c14, r2c15,         \
               #r2c9,  r3c10, r3c11, r3c12, r3c13, r3c14, r3c15,         \
               #r3c8,  r2c8,  r1c8, r0c8,                                \
               #r3c9)                                                    \
  #{                                                                     \
    #{r0c0, r0c1, r0c2, r0c3, r0c4, r0c5, r0c6, r0c7, r0c8, r0c9, r0c10, r0c11, r0c12, r0c13, r0c14, r0c15}, \
    #{r1c0, r1c1, r1c2, r1c3, r1c4, r1c5, r1c6, r1c7, r1c8, r1c9, r1c10, r1c11, r1c12, r1c13, r1c14, r1c15}, \
    #{r2c0, r2c1, r2c2, r2c3, r2c4, r2c5, r2c6, r2c7, r2c8, r2c9, r2c10, r2c11, r2c12, r2c13, r2c14, r2c15}, \
    #{r3c0, r3c1, r3c2, r3c3, r3c4, r3c5, r3c6, r3c7, r3c8, r3c9, r3c10, r3c11, r3c12, r3c13, r3c14, r3c15}, \
  #}