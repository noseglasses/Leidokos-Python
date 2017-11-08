# Kaleidoscope-Python-Wrapper
This plugin generates python wrapper code for other Kaleidoscope modules.

# Mode of operation
This plugin depends on the [Kaleidoscope-Hardware-Virtual](https://github.com/cdisselkoen/Kaleidoscope-Hardware-Virtual) plugin
to build a shared library that can loaded as a python module on the host system (x86).
The build process is too complex to be incorporated in the Arduino build system.
To automatize largest parts of the build process, the plugin relies on
[CMake](https://cmake.org/) as its build system.

A two step build process consists in running CMake to setup the Kaleidoscope
build system and then executing the Arduino build system of the overall sketch.
The following explanation assumes that a firmware setup has been created, 
as described in the [Kaleidoscope Wiki](https://github.com/keyboardio/Kaleidoscope/wiki/Keyboardio-Model-01-Introduction).

1. To be build relying on the external boost and python includes and libraries.
Boost and python are automatically detected and the build system can be 
configurated if one of the dependencies is installed in a non-standard location.

```
cd <sketchbook_dir>/hardware/keyboardio/avr/libraries
git clone https://github.com/noseglasses/Kaleidoscope-Python-Wrapper.git
cd Kaleidoscope-Python-Wrapper
cmake -DKALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR=<sketchbook_dir> \
      -DKALEIDOSCOPE_MODULE_REPO_PATHS=<sketchbook_dir>/hardware/keyboardio/avr/libraries \
      .
```

2. Once the CMake process executed, the firmware can be build as follows
```
cd <sketchbook_dir>/Model01-Firmware
BOARD=virtual make
```

TODO: This will create a library ... in ... that can be used as a python module.

TODO: Describe loading python

# Prerequisites
Python wrapping depends on [boost python](http://www.boost.org) to auto generate 
python wrapper code for C++ classes, functions and global data. Also, CMake is 
needed to setup the plugin's build system.

On Ubuntu Linux, the necessary packages can be installed as
```
sudo apt-get install libboost-python-dev cmake
```
To configure the CMake build system manually, most Linux distributions allow 
for a curses based CMake GUI to be installed. Under Ubuntu install it as follows. 
```
sudo apt-get install cmake-curses-gui
```
This is how to execute the CMake GUI.
```
cd <sketchbook_dir>/hardware/keyboardio/avr/libraries/Kaleidoscope-Python-Wrapper
ccmake .
```

# CMake build setup configuration
The CMake based setup of the plugin's Arduino build relies on a number of 
variables that allow detailed configuration. Run `ccmake .` as described above and 
look for build variables whose name starts with `KALEIDOSCOPE_`. Every 
variable comes with a detailed description.

# Python export
The plugin allows any Kaleidscope components to export classes, functions and 
data to be accessible from python scripts. The easiest way for this 
to work is to add a file named `<suitable_name>.python-wrapper` to the
`src` directory of any module. 

The `.python-wrapper` are actually C++ files
that use a different file extension to prevent them to be considered in any builds
that are not be meant on the host system (x86). To make them accessible 
in the latter case, the plugin's CMake system detects all `.python-wrapper` files
and generates alias files (symbolic links) that are appended the extension `.cpp`.

An example `.python-wrapper` file that exports the `Layer_` class of the
Kaleidoscope core could look the following way. See the [documentation
of boost-python](http://www.boost.org/doc/libs/1_58_0/libs/python/doc/index.html)
for more information.

```cpp
// Content of Kaleidoscope/src/Kaleidoscope.python-wrapper
#include <boost/python.hpp>

#include "layers.h"
#include <stdint.h>

using namespace boost::python;
   
#define EXPORT_STATIC_METHOD(NAME) .def(#NAME, &Layer_::NAME)

BOOST_PYTHON_MODULE(kaleidoscope)
{
    class_<Layer_>("Layer")
      EXPORT_STATIC_METHOD(lookup)
      EXPORT_STATIC_METHOD(lookupOnActiveLayer)
      EXPORT_STATIC_METHOD(on)
      EXPORT_STATIC_METHOD(off)
      EXPORT_STATIC_METHOD(move)
      EXPORT_STATIC_METHOD(top)
      EXPORT_STATIC_METHOD(next)
      EXPORT_STATIC_METHOD(previous)
      EXPORT_STATIC_METHOD(isOn)
      EXPORT_STATIC_METHOD(getLayerState)
      EXPORT_STATIC_METHOD(eventHandler)
      EXPORT_STATIC_METHOD(getKeyFromPROGMEM)
      EXPORT_STATIC_METHOD(updateLiveCompositeKeymap)
      EXPORT_STATIC_METHOD(updateActiveLayers)
      
      // As there are two overloaded versions of 
      // defaultLayer that are actually a getter and a setter, we have 
      // to point the compiler to the different versions of the functions
      // by casting to the different function pointer types
      //
      .def("getDefaultLayer", static_cast< 
            uint8_t(*)()
         >(&Layer_::defaultLayer)
      )
      .def("getDefaultLayer", static_cast< 
            void(*)(uint8_t)
         >(&Layer_::defaultLayer)
      )
    ;
}
```