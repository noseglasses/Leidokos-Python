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

#ifndef KPV_LOGGING_HPP
#define KPV_LOGGING_HPP

// #define KPV_HAVE_LOGGING

#ifdef KPV_HAVE_LOGGING
#include <iostream>

   #define KPV_LOG(...) std::cout << "*** " << __VA_ARGS__ \
      << " (" __FILE__ << ":" << __LINE__ << ")" << std::endl;
#else // #ifdef KPV_HAVE_LOGGING
   #define KPV_LOG(...)
#endif // #ifdef KPV_HAVE_LOGGING

#endif
