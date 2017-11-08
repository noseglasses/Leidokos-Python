# Kaleidoscope-Python-Wrapper
This plugin generates Python wrapper code for other Kaleidoscope modules.
It creates a shared library that can be loaded as a Python module. 

This is an auxiliary plugin in a sense that is meant to be integrated in 
testing toolchains on the host system (x86). It does not provide any 
features for the actual firmware.

# Mode of operation
This plugin depends on the [Kaleidoscope-Hardware-Virtual](https://github.com/cdisselkoen/Kaleidoscope-Hardware-Virtual) plugin
to build a shared library that can be loaded as a Python module on the host system (x86).
Its build process is too complex to be entirely incorporated in the Arduino build system.
Therefore, to automatize largest parts of the build process, the plugin relies on
[CMake](https://cmake.org/) as a first level build system that prepares 
the actual build as part of the Arduino build system.

A two step build process consists in running CMake to prepare the plugin's build 
system and that of all modules that request the generation of Python wrappers.
In a second step, the Arduino build system of the overall sketch is executed
that creates the loadable Python module that makes all those modules accessible
to Python that have specified directives for wrapper generation, see
more about this below.

# How to build

The following explanation of the Python module build 
assumes that a firmware setup has already been established in a directory `<sketchbook_dir>`, 
as described in the [Kaleidoscope Wiki](https://github.com/keyboardio/Kaleidoscope/wiki/Keyboardio-Model-01-Introduction).

1. The CMake setup process automatically detects Boost Python and a 
Python installation and prepares all plugins that reside in one or more
directories that are specified through the CMake variable `KALEIDOSCOPE_MODULE_REPO_PATHS`.
It also prepares the overall build system by generating symbolic links
in specific places. The latter is necessary to allow for builds that
can run on the host system (x86) rather than the keyboard.

```
cd <sketchbook_dir>/hardware/keyboardio/avr/libraries
git clone https://github.com/noseglasses/Kaleidoscope-Python-Wrapper.git
cd Kaleidoscope-Python-Wrapper
cmake -DKALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR=<sketchbook_dir> \
      -DKALEIDOSCOPE_MODULE_REPO_PATHS=<sketchbook_dir>/hardware/keyboardio/avr/libraries \
      .
```

2. Build the Python model by running the Arduino firmware build process for 
the virtual hardware.
```
cd <sketchbook_dir>/Model01-Firmware
BOARD=virtual make
```

TODO: This will create a library ... in ... that can be used as a Python module.

# Prerequisites
Python wrapping depends on [boost Python](http://www.boost.org) to auto-generate 
Python wrapper code for C++ classes, functions and global data. Appart from that, CMake is 
needed to setup the plugin's build system.

On Ubuntu Linux, the necessary packages can be installed as
```
sudo apt-get install libboost-Python-dev cmake
```
To configure the CMake build system manually, most Linux distributions allow 
for a curses based CMake GUI to be installed. Install it as follows under Ubuntu Linux. 
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
variables that allow detailed configuration. For an explanation of such 
variables, run `ccmake .` as described above. Then look for build variables 
whose name starts with `KALEIDOSCOPE_`. A documentation of a variable
is shown when the cursor is moved to the variable's line.

# Python export
The plugin allows any Kaleidscope components to export classes, functions and 
data to be accessible from Python scripts. The easiest way for this 
to work is to add a file named `<your_module_name>.Python-wrapper` to the
`src` directory of any Kaleidscope module that is meant to export symbols
to python language. 

The `.Python-wrapper` are actually C++ files. We use
a different file extension to prevent them to be considered in any builds
that are not targeted to the host system (x86). To make them accessible
for the Python wrapper build, the plugin's CMake system detects any `.Python-wrapper` files
in directories that reside below paths that are 
specified in `KALEIDOSCOPE_MODULE_REPO_PATHS`. For all files found,
alias files (symbolic links) are generated. To allow them to be
found during the actual firmware build, we append the extension `.cpp`
to the original `.Python-wrapper` filename.

An example `.Python-wrapper` file that exports the `Layer_` class of the
Kaleidoscope core could look the following way. See the [documentation
of boost-Python](http://www.boost.org/doc/libs/1_58_0/libs/Python/doc/index.html)
for more information.

```cpp
// Content of Kaleidoscope/src/Kaleidoscope.Python-wrapper

#include <boost/Python.hpp>

#include "layers.h"
#include <stdint.h>

using namespace boost::Python;
   
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

# Python module usage
TODO: Describe loading Python