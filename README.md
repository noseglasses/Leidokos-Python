![status][st:experimental] [![Build Status][travis:image]][travis:status]

[travis:image]: https://travis-ci.org/noseglasses/Kaleidoscope-Python-Wrapper.svg?branch=master
[travis:status]: https://travis-ci.org/noseglasses/Kaleidoscope-Python-Wrapper

[st:stable]: https://img.shields.io/badge/stable-✔-black.svg?style=flat&colorA=44cc11&colorB=494e52
[st:broken]: https://img.shields.io/badge/broken-X-black.svg?style=flat&colorA=e05d44&colorB=494e52
[st:experimental]: https://img.shields.io/badge/experimental----black.svg?style=flat&colorA=dfb317&colorB=494e52

# Kaleidoscope-Python-Wrapper
This project provides a Python interface to a virtual Kaleidoscope firmware.
It can be used to prototype new or to test existing functionality, e.g.
as part of a regression-testing framework.

Python wrapper code is generated for the main firmware as well as
for plugins that explicitly support Python code export. The virtual firmware
can be loaded as a Python module.

# Example usage
Below you see the python code of the example `examples/test_kaleidoscope.py` that is
provided as part of the project source repository. It tests some functionality
of the firmware.

```python
import kaleidoscope

from kaleidoscope import *

import sys

test = Test()
test.debug = True

# The assertions are evaluated in the next loop cycle
#
test.queueGroupedReportAssertions([ 
      ReportNthInCycle(1), 
      ReportNthCycle(1),
      ReportKeyActive(keyA()),
      ReportKeyActive(keyB()),
      ReportModifierActive(modSHIFT_HELD()),
      DumpReport()
   ])

test.keyDown(2, 1)

test.scanCycle()

test.keyUp(2, 1)

test.scanCycles(2)

test.skipTime(200)
```

The test deliberately fails. It's console output (stdout) is the following.

```
################################################################################

Kaleidoscope-Python-Wrapper

author: noseglasses (https://github.com/noseglasses, shinynoseglasses@gmail.com)
version: e53109d519c6041e595a441d98957a71a7661129

cycle duration: 5.000000
################################################################################

0000000000 Single scan cycle
0000000000    Scan cycle 1
0000000000       Processing keyboard report 1 (1. in cycle)
0000000000          1 queued report assertions
0000000000             Report assertion passed: Is 1. report in cycle
0000000000             Report assertion passed: Is 1. cycle
0000000000             Report assertion passed: Key A active
0000000000             !!! Report assertion failed: Key B active
0000000000             !!! Report assertion failed: Modifier SHIFT_HELD active
0000000000             Report assertion passed: Dump report: a 
0000000000       1 keyboard reports processed
0000000005 
0000000005 Running 2 cycles
0000000005    Scan cycle 2
0000000005       Processing keyboard report 2 (1. in cycle)
0000000005          0 queued report assertions
0000000005       1 keyboard reports processed
0000000010    Scan cycle 3
0000000010       No keyboard reports processed
0000000015 
0000000015 Skipping dt >= 20.000000 ms
0000000015    Scan cycle 4
0000000015       No keyboard reports processed
0000000020    Scan cycle 5
0000000020       No keyboard reports processed
0000000025    Scan cycle 6
0000000025       No keyboard reports processed
0000000030    Scan cycle 7
0000000030       No keyboard reports processed
0000000035    20.000000 ms (4 cycles) skipped
0000000035 

################################################################################
Testing done
################################################################################

!!! Error: Not all assertions passed
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!! Error: Terminating with exit code 1
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```
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

# How to use

The following explanation of the Python module build 
assumes that a firmware setup has already been established in a directory `<sketchbook_dir>`, 
as described in the [Kaleidoscope Wiki](https://github.com/keyboardio/Kaleidoscope/wiki/Keyboardio-Model-01-Introduction).

1. The CMake setup process automatically detects Boost Python and a 
Python installation and prepares all plugins that reside in one or more
directories that are specified through the CMake variable `KALEIDOSCOPE_HARDWARE_BASE_PATH`.
It also prepares the overall build system by generating symbolic links
in specific places. The latter is necessary to allow for builds that
can run on the host system (x86) rather than the keyboard.

```bash
SKETCHBOOK_DIR=<sketchbook_dir>
BUILD_DIR=<build_dir>

cd $SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries

git clone https://github.com/noseglasses/Kaleidoscope-Python-Wrapper.git
git clone https://github.com/keyboardio/Kaleidoscope-Hardware-Virtual.git

cd ${BUILD_DIR}
      
cmake \
   -DKALEIDOSCOPE_HARDWARE_BASE_PATH=$SKETCHBOOK_DIR/hardware \
   -DKALEIDOSCOPE_LIBRARIES_DIR=$SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries \
   -DKALEIDOSCOPE_FIRMWARE_SKETCH=$SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries/Model01-Firmware/Model01-Firmware.ino \
   $SKETCHBOOK_DIR/hardware//keyboardio/avr/libraries/Kaleidoscope-Python-Wrapper
```

2. Build the Python model by running the build processed as described 
for [Kaleidoscope-CMake](https://github.com/noseglasses/Kaleidoscope-CMake.git), e.g.

```bash
make
```

This will create a library `kaleidoscope.so` or `kaleidoscope.dll` in 
the build directory that is actually a Python module.

3. Run an example firmware test

```bash
export PYTHONPATH=$BUILD_DIR:$SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries/Kaleidoscope-Python-Wrapper/python:$PYTHONPATH
python $SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries/Kaleidoscope-Python-Wrapper/test_kaleidoscope.py
```


# Prerequisites
Python wrapping depends on [boost Python](http://www.boost.org) to auto-generate 
Python wrapper code for C++ classes, functions and global data. Appart from that, CMake is 
needed to setup the plugin's build system.

On Ubuntu Linux, the necessary packages can be installed as
```bash
sudo apt-get install libboost-Python-dev cmake
```
To configure the CMake build system manually, most Linux distributions allow 
for a curses based CMake GUI to be installed. Install it as follows under Ubuntu Linux. 
```bash
sudo apt-get install cmake-curses-gui
```
This is how to execute the CMake GUI.
```bash
cd <sketchbook_dir>/hardware/keyboardio/avr/libraries/Kaleidoscope-Python-Wrapper
ccmake .
```
For the generation of the Python API generation, you will have to install 
[http://www.sphinx-doc.org](Sphinx), under Ubuntu Linux e.g. as
```bash
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
| KALEIDOSCOPE_PYTHON_GENERATE_API_DOC | Enable this flag to generate the Python API documentation |

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

```bash
export PYTHONPATH=<path to kaleidoscope.so>:<Kaleidoscope-Python-Wrapper repo path>/python:$PYTHONPATH
```
You can then run one of the examples or your own python test script, e.g.
```bash
<Kaleidoscope-Python-Wrapper repo path>/examples/test_kaleidoscope.py
```

# Python API documentation
HTML based documentation of the Python API supplied by Kaleidoscope-Python-Wrapper 
can be auto-generated through the CMake `doc` target. Please see the 
Prerequisites section of this documentation for information about 
additional third party software that needs to be installed on you platform
to generate the API documentation.

Configure the build system as explained above but add the flag
```bash
cmake ... \
   -DKALEIDOSCOPE_PYTHON_GENERATE_API_DOC=TRUE
```
*Note:* You can also enable the variable `KALEIDOSCOPE_PYTHON_GENERATE_API_DOC`
from the CMake curses GUI (ccmake) or other CMake GUIs.

Then build the API documentation. When the GNU Makefile 
generator is used (the default under Linux), this can e.g. be done as follows.
```bash
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
