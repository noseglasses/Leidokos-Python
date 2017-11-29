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
directories that are specified through the CMake variable `KALEIDOSCOPE_HARDWARE_BASE_PATH`.
It also prepares the overall build system by generating symbolic links
in specific places. The latter is necessary to allow for builds that
can run on the host system (x86) rather than the keyboard.

```
cd <sketchbook_dir>/hardware/keyboardio/avr/libraries
git clone https://github.com/noseglasses/Kaleidoscope-Python-Wrapper.git
cd Kaleidoscope-Python-Wrapper
cmake -DKALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR=<sketchbook_dir> \
      -DKALEIDOSCOPE_MODULE_REPO_PATHS=<sketchbook_dir>/hardware/keyboardio/avr/libraries \
      
cmake \
   -DKALEIDOSCOPE_HARDWARE_BASE_PATH=<path to the firmware hardware directory> \
   -DKALEIDOSCOPE_ARCHITECTURE_ID=x86 \
   -DKALEIDOSCOPE_BOARD=virtual \
   -DKALEIDOSCOPE_HOST_BUILD=TRUE \
   -DKALEIDOSCOPE_LIBRARIES_DIR=<path to the firmware hardware directory>/keyboardio/avr/libraries \
   -DKALEIDOSCOPE_FIRMWARE_SKETCH=<Path to the .ino file> \
   <The path to the Kaleidoscope-Python-Wrapper repo>
      .
```

2. Build the Python model by running the build processed as described 
for [Kaleidoscope-CMake](https://github.com/noseglasses/Kaleidoscope-CMake.git), e.g.

```
make
```

This will create a library `kaleidoscope.so` or `kaleidoscope.dll` in 
the build directory that is actually a Python module.

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
For the generation of the Python API generation, you will have to install 
[http://www.sphinx-doc.org](Sphinx), under Ubuntu Linux e.g. as
```
sudo apt-get install python-sphinx
```

# CMake build setup configuration
The CMake based setup of the plugin's Arduino build relies on a number of 
variables that allow detailed configuration. For an explanation of such 
variables, run `ccmake .` as described above. Then look for build variables 
whose name starts with `KALEIDOSCOPE_`. A documentation of a variable
is shown when the cursor is moved to the variable's line.

Although, Kaleidoscope-Python-Wrapper is meant to be as auto-detecting and smart as possible,
it may be necessary to configure the system.

| CMake Variable                  | Purpose                                                           |
|:------------------------------- |:----------------------------------------------------------------- |
| KALEIDOSCOPE_MODULE_REPO_PATHS  | The base below which Kaleidoscope module repos live that might contain `.python-wrapper` files |
| KALEIDOSCOPE_MODULE_REPO_PATHS_FILE | A text file that contains path names (linewise) of Kaleidoscope module repos that might contain `.python-wrapper` files |
| KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR | A path to an Arduino sketchbook. |

Other variables are defined by [Kaleidoscope-CMake](https://github.com/noseglasses/Kaleidoscope-CMake.git)
and documented there.

# Python module usage
Kaleidoscope-Python-Wrapper provides a Python API that makes the generation
of Kaleidoscope firmare tests pretty simple.

The API lives in a python module `kaleidoscope_testing` that can be found 
in the `python` directory of the Kaleidoscope-Python-Wrapper repository.

Examples that exemplify the use of the testing API can be found in the `examples`
directory.

For Python to find the generated firmware module and the the `kaleidoscope_testing`
module. Both files' paths must be made known to Python via the environment 
variable `PYTHONPATH`, e.g. as

```
export PYTHONPATH=<path to kaleidoscope.so>:<Kaleidoscope-Python-Wrapper repo path>/python:$PYTHONPATH
```
You can then run one of the examples or your own python test script, e.g.
```
<Kaleidoscope-Python-Wrapper repo path>/examples/test_kaleidoscope.py
```

# Python API documentation
HTML based documentation of the Python API supplied by Kaleidoscope-Python-Wrapper 
can be auto-generated through the CMake `doc` target. Please see the 
Prerequisites section of this documentation for information about 
additional third party software that needs to be installed on you platform
to generate the API documentation.

When the GNU Makefile 
generator is used (the default under Linux), this can be done as follows.
```
make doc
```
The documentation is generated in the `doc/kaleidoscope` directory of 
the build tree. Open the file `kaleidoscope_testing.html` in a browser
to see the API documentation.

# Python export
The plugin allows any Kaleidscope components to export classes, functions and 
data to be accessible from Python scripts. The easiest way for this 
to work is to add a file named `<your_module_name>.python-wrapper` to the
`src` directory of any Kaleidscope module that is meant to export symbols
to python language. 

The `.python-wrapper` are actually C++ files. We use
a different file extension to prevent them to be considered in any builds
that are not targeted to the host system (x86). To make them accessible
for the Python wrapper build, the plugin's CMake system detects any `.python-wrapper` files
in directories that reside below paths that are 
specified in `KALEIDOSCOPE_MODULE_REPO_PATHS`. For all files found,
alias files (symbolic links) are generated. To allow them to be
found during the actual firmware build, we append the extension `.cpp`
to the original `.python-wrapper` filename.

An example `.python-wrapper` file that exports the `Layer_` class of the
Kaleidoscope core could look the following way. See the [documentation
of boost-Python](http://www.boost.org/doc/libs/1_58_0/libs/Python/doc/index.html)
for more information.

```cpp
// Content of Kaleidoscope/src/Kaleidoscope.python-wrapper

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
