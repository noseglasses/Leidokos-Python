![status][st:experimental]
[![Build Status][travis:linux:image]][travis:linux:target]
[![Build Status][travis:MacOS:image]][travis:MacOS:target]
[![Latest version][version:image]][version:target]

[![Python API documentation][python:api:image]][python:api:target]

[travis:linux:image]: https://img.shields.io/travis/CapeLeidokos/Leidokos-Python.svg?style=for-the-badge&label=Linux&branch=master
[travis:linux:target]: https://travis-ci.org/CapeLeidokos/Leidokos-Python

[travis:MacOS:image]: https://img.shields.io/travis/CapeLeidokos/Leidokos-Python.svg?style=for-the-badge&label=Mac&branch=master
[travis:MacOS:target]: https://travis-ci.org/CapeLeidokos/Leidokos-Python

[version:image]: https://img.shields.io/github/release/CapeLeidokos/Leidokos-Python.svg?style=for-the-badge
[version:target]: https://github.com/CapeLeidokos/Leidokos-Python/releases

[st:stable]: https://img.shields.io/badge/stable-✔-black.svg?style=for-the-badge&colorA=44cc11&colorB=494e52
[st:broken]: https://img.shields.io/badge/broken-X-black.svg?style=for-the-badge&colorA=e05d44&colorB=494e52
[st:experimental]: https://img.shields.io/badge/experimental----black.svg?style=for-the-badge&colorA=dfb317&colorB=494e52

[python:api:image]: https://img.shields.io/badge/Python-API-ff69b4.svg?style=for-the-badge
[python:api:target]: https://capeleidokos.github.io/Leidokos-Python/API/index.html

# Leidokos-Python
Leidokos-Python is a Python scriptable Kaleidoscope firmware simulator.

## Introduction
Leidokos-Python can be used to prototype new or to test existing functionality, e.g.
as part of a regression-testing framework.

Python wrapper code is generated for the main firmware as well as
for plugins that explicitly support Python code export. The virtual firmware
can be loaded as a Python module.

The project aims to support all portable features of the firmware to make it
possible to develop new plugins in a rapid and painless way before finally porting them to C++.
Sometimes implementations are the only way to test weird ideas and new algorithms.
Leidokos-Python helps by allowing to test such new features under reproducible lab conditions.

## About this document
Leidokos-Python is an open source project whose documentation is and will be a work in progress. If you find any errors or sections that might be improved, please don't hesitate to generate an issue or pull request on [GitHub](https://github.com/CapeLeidokos/Leidokos-Python).

## CapeLeidokos
Leidokos-Python is an essential part of the CapeLeidokos build, develop and testing infrastructure for the Kaleidoscope firmware.

<img src="https://github.com/CapeLeidokos/CapeLeidokos/blob/master/CapeLeidokos.svg?sanitize=true">

# Example usage
Below you see the python code of the example `examples/test_kaleidoscope.py` that is
provided as part of the project source repository. It tests some functionality
of the firmware.

```python
import kaleidoscope

from kaleidoscope import *

import sys

driver = TestDriver()
driver.debug = True

# The assertions are evaluated in the next loop cycle
#
driver.queueGroupedReportAssertions([
      ReportNthInCycle(1),
      ReportNthCycle(1),
      ReportKeyActive(keyA()),
      ReportKeyActive(keyB()),
      ReportModifierActive(modSHIFT_HELD()),
      DumpReport()
   ])

driver.keyDown(2, 1)
driver.scanCycle()
driver.keyUp(2, 1)
driver.scanCycles(2)
driver.skipTime(200)
```

Although this might sound strange, tests are there to (potentially) fail. A test that fails helps you to fix an issue in your software. You will rarely look at the output of tests that pass, but if a test fails you certainly want to know what exactly went wrong. That's why it is so important that the information provided by a regression system is more than just to inform that a specific test failed.

To demonstrate what Leidokos-Python outputs when a test fails, this example is deliberately build to fail.

It's console output (stdout) is the following.

```
################################################################################

Leidokos-Python

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

# A virtual keyboard

A keyboard firmware is an endless program that reacts in real time on user input.
The real time aspect makes it sometimes very difficult to debug or test certain
aspects of a firmware where timing is very important. On a real hardware it is sometimes necessary to hid several keys in a well defined order to trigger a specific behavior (e.g. to reproduce a bug). This can require skills that only a professional pianist would have.

This is where Leidokos-Python comes in quite handy.

## Reproducible key sequences
Leidokos-Python enables an exact and reproducible simulation of
the firmware input in terms of key-action sequences (presses and releases). Once setup the sequence can be repeated as often as necessary while debugging and changing the firmware code.

## Virtual scan cycles
Key-actions alone would not suffice to simulate the behavior of a real keyboard run.
The firmware is essentially an endless loop where every cycle checks the current state of the keyboard matrix and triggers events by calling hook functions (scan cycle).

The actual timing in the simulation is define by specifying how many keyboard scan cycles do elapse between key actions. Leidokos-Python allows to specify counts of scan cycles but also amounts of time that are supposed to elapse while virtual firmware is performing can cycles. The latter is possible if there is an estimate of the time a single scan cycle takes to execute on the real hardware (typically in the order of few milliseconds). Leidokos-Python automatically computes the number of cycles that match a given time interval.

## Runtime assertions
As a reaction on key actions, the firmware generates USB HID reports. These reports are the firmware's output data. It is therefore important to carefully observe the firmware's
I/O behavior. To simplify this, Leidokos-Python provides a large set of
runtime assertions that can be used to define exactly what output is expected as a reaction on specific key-events. Assertions are grouped in report assertions and process assertions.

### Report assertions
A report assertion basically verifies specific properties of a key report, e.g. must contain a certain key or modifier or must not contain. Any combinations are possible.
Report assertions can be grouped and queued. Whenever a report is generated by the keyboard firmware, the next group of assertions is taken form the queue, applied to the report and then discarded.
When assertions fail, errors are reported.

### Process assertions
Process assertions are there to ensure correct timing. This is the main difference when compared to report assertions which are agnostic to the concept of time.
A process assertion can e.g. check if between two control points of the test run a specific number of reports have been generated.

## Python inter-operation with the firmware
By means of Python export, the firmware and all of its plugins can make symbols (functions and variables) available to Python. This means that you can actually call firmware functions from the python side. This can be very valuable when writing tests to assert specific properties or to control the firmware state but also to
play with the firmware without touching the C++ code. The latter allows for much faster development cycles.

## Virtual plugins
Leidokos-Python by itself exports most symbols of the Kaleidoscope core as Python code. This enables to implement whole plugins as Python code for virtual prototyping.
It is much faster to develop a new algorithm in Python than in C++ due to the absence of compile and upload.

## Test driven development
You have a new idea and want to write a Kaleidoscope plugin to realize it.
Why not use test driven development. The following process can drastically shorten development times.

1. Define a set of tests with Leidokos-Python.
2. Develop the plugin's algorithm as Python code.
3. Run the virtual firmware and debug your code until all your tests pass.
4. Port the plugin's Python code to C++.
5. Run the test series again with the C++ version of the new plugin.
6. Upload and test on the real hardware.
7. Use and maintain the already existing tests for regression testing with [Leidokos-Testing](https://github.com/CapeLeidokos/Leidokos-Testing).

## Debugging
Most people develop firmware software in change-compile-upload-test cycles.
In such a scenario, the only way to debug is passing back `printf`-type output to the host system or to use other type of feedback, like LEDs or sounds to report the state of the device. But how to debug e.g. segmentation faults?

Using Leidokos-Python using a debugger is very simple. Just run the whole python process in your favorite debugger. This enables you to debug the firmware code as if it was a host program. Leidokos-Python's programmable tests enable an exact reproducibility of errors.

# Usage

The following explanation of the Python module build
assumes that a firmware setup has already been established in a directory `<sketchbook_dir>`,
as described in the [Kaleidoscope Wiki](https://github.com/keyboardio/Kaleidoscope/wiki/Keyboardio-Model-01-Introduction).

This example works on GNU/Linux and MacOS.

__Important:__ During development, you would only repeat steps 2. and 3. in a change-test cycles.

## 1. Configure the CMake build system

Configuration of the build system is only carried out once. Later you will
only repeat the build process while developing.

The CMake configuration process automatically detects Boost Python and a
Python installation and prepares all plugins that reside in one or more
directories that are specified through the CMake variable `KALEIDOSCOPE_HARDWARE_BASE_PATH`.
It also prepares the overall build system by generating symbolic links
in specific places. The latter is necessary to allow for builds that
can run on the host system (x86) rather than the keyboard.

```bash
# Set some auxiliary variables that will be used later on.
#
SKETCHBOOK_DIR=<sketchbook_dir>
BUILD_DIR=<build_dir>

# Clone Leidokos-Python to your firmware boards directory.
#
cd $SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries
git clone --recursive https://github.com/CapeLeidokos/Leidokos-Python.git

# Run the CMake configuration process.
#
cd ${BUILD_DIR}
cmake \
   -DKALEIDOSCOPE_FIRMWARE_SKETCH=$SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries/Model01-Firmware/Model01-Firmware.ino \
   $SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries/Leidokos-Python
```

## 2. Build the Firmware

Build the firmware as described
for [Leidokos-CMake](https://github.com/CapeLeidokos/Leidokos-CMake.git), on a GNU/Linux or MacOS system e.g. run

```bash
make
```

This will create a library `kaleidoscope.so` (GNU/Linux and MacOS) or `kaleidoscope.dll` (Windows) in
the build directory. The shared library (dll) that is created will be loaded as a Python module during you tests.

## 3. Run a virtual firmware

```bash
# Tell Python where to find the newly build module and some auxiliary modules
# that come with Leidokos-Python.
#
export PYTHONPATH=$BUILD_DIR:$SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries/Leidokos-Python/python:$PYTHONPATH

# Run the Python test.
#
python $SKETCHBOOK_DIR/hardware/keyboardio/avr/libraries/Leidokos-Python/test_kaleidoscope.py
```


# Under the hood
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

# Prerequisites

Leidokos-Python depends on a number of external software projects to build and
run firmware. The installation process greatly differs between platforms and OS flavors.

It is not possible for Leidokos-Python's maintainers to support all sorts of
platforms. Build instructions might change over time. Whenever you find that the instructions in this document are out of date, please open an [issue or submit a pull request](https://github.com/CapeLeidokos/Leidokos-Python).

## GUN/Linux
Python wrapping depends on [boost Python](http://www.boost.org) to auto-generate
Python wrapper code for C++ classes, functions and global data. Apart from that, CMake is
needed to setup the plugin's build system.

On Ubuntu Linux, the necessary packages can be installed as
```bash
sudo apt-get install libboost-python-dev cmake
```
To configure the CMake build system manually, most Linux distributions allow
for a curses based CMake GUI to be installed. Install it as follows under Ubuntu Linux.
```bash
sudo apt-get install cmake-curses-gui
```
This is how to execute the CMake GUI.
```bash
cd <sketchbook_dir>/hardware/keyboardio/avr/libraries/Leidokos-Python
ccmake .
```
For the generation of the Python API generation, you will have to install
[http://www.sphinx-doc.org](Sphinx), under Ubuntu Linux e.g. as
```bash
sudo apt-get install python-sphinx
```
## MacOS
Prerequisites can be installed using [homebrew](https://brew.sh/).
```bash
brew install ccache
brew install python3
brew install boost-python --with-python3 --without-python
sudo -H pip3 install pyyaml
sudo -H pip3 install sphinx
```

## Windows
Currently there is no official Windows support. All required prerequisites are available for Windows, we just haven't found time to come up with build instructions.

If you find a way to use Leidokos-Python with Windows, please let us know by submitting an [issue or a pull request](https://github.com/CapeLeidokos/Leidokos-Python).

# CMake build setup configuration
The CMake based setup of the plugin's Arduino build relies on a number of
variables that allow detailed configuration. For an explanation of such
variables, run `ccmake .` as described above. Then look for build variables
whose name starts with `KALEIDOSCOPE_`. A documentation of a variable
is shown when the cursor is moved to the variable's line.

Although, Leidokos-Python is meant to be as auto-detecting and smart as possible,
it may be necessary to configure the system.

| CMake Variable                  | Purpose                                                           |
|:------------------------------- |:----------------------------------------------------------------- |
| KALEIDOSCOPE_MODULE_REPO_PATHS  | The base below which Kaleidoscope module repositories live that might contain `.python-wrapper` files |
| KALEIDOSCOPE_MODULE_REPO_PATHS_FILE | A text file that contains path names (linewise) of Kaleidoscope module repos that might contain `.python-wrapper` files |
| KALEIDOSCOPE_ARDUINO_SKETCHBOOK_DIR | A path to an Arduino sketchbook. |
| LEIDOKOS_PYTHON_GENERATE_API_DOC | Enable this flag to generate the Python API documentation |

Other CMake build system variables are defined by [Leidokos-CMake](https://github.com/CapeLeidokos/Leidokos-CMake.git)
and documented there.

# Python module usage
Leidokos-Python provides a Python API that makes the generation
of Kaleidoscope firmware tests pretty simple.

The API lives in a python module `leidokos` that can be found
in the `python` directory of the Leidokos-Python repository.

Examples that exemplify the use of the testing API can be found in the `examples`
directory of this project.

For Python to find the generated firmware module and the the `leidokos`
module. Both files' paths must be made known to Python via the environment
variable `PYTHONPATH`, e.g. as

```bash
export PYTHONPATH=<path to kaleidoscope dynamic library>:<Leidokos-Python repo path>/python:$PYTHONPATH
```
You can then run one of the examples or your own python test script, e.g.
```bash
PYTHON3_EXECUTABLE=<path_to_your_python_3_executable>/python3
LEIDOKOS_PYTHON_REPOSITORY=<Leidokos_Python_repo_path>

$PYTHON3_EXECUTABLE $LEIDOKOS_PYTHON_REPOSITORY/examples/test_kaleidoscope.py
```

# Python API documentation
HTML based documentation of the Python API supplied by Leidokos-Python
can be auto-generated through the CMake `doc` target. Please see the
Prerequisites section of this documentation for information about
additional third party software that needs to be installed on you platform
to generate the API documentation.

Configure the build system as explained above but add the flag
```bash
cmake ... \
   -DLEIDOKOS_PYTHON_GENERATE_API_DOC=TRUE
```
*Note:* You can also enable the variable `LEIDOKOS_PYTHON_GENERATE_API_DOC`
from the CMake curses GUI (ccmake) or other CMake GUIs.

Then build the API documentation. When the GNU Makefile
generator is used (the default under Linux), this can e.g. be done as follows.
```bash
make doc
```
The documentation is generated in the `doc/kaleidoscope/API` directory of
the build tree. Open the file `kaleidoscope_testing.html` in a browser
to see the API documentation.

# Python export
Leidokos-Python allows any Kaleidoscope components to export classes, functions and
data to be accessible from Python scripts. The easiest way for this
to work is to add a file named `<your_module_name>.python-wrapper` to the
`src` directory of any Kaleidoscope module that is meant to export symbols
to python language.

The `.python-wrapper` are actually C++ files. We use
a different file extension to prevent them to be considered in any normal firmware builds
that are not targeted to the host system (x86). To make them accessible
for the Python wrapper build, the plugin's CMake system searches for `.python-wrapper` files
in directories below paths that are
specified in `KALEIDOSCOPE_MODULE_REPO_PATHS`. For all files found,
symbolic links with extension `.cpp` are generated to allow the python wrapper files to be found during the actual firmware build.

An example `.python-wrapper` file that exports the `MouseKeys_` class of
plugin *Kaleidoscope-MouseKeys* might look the following way. See the [documentation
of boost-Python](http://www.boost.org/doc/libs/1_58_0/libs/Python/doc/index.html)
for more information.

__Important:__ The Kaleidoscope-MouseKeys plugin may have changed after this document was written. This example simply demonstrates how an export for
a plugin might look.

For a real example have a look on the `testing/example_test` directory of CapeLeidokos' fork of [Kaleidoscope-OneShot](https://github.com/CapeLeidokos/Kaleidoscope-OneShot/tree/feature/python_export) which is a demo regression system setup. Also have a look at the project's `.travis.yml` file to see how Leidokos-Testing is used for regression testing.

```cpp
// Content of Kaleidoscope-MouseKeys/src/Kaleidoscope.python-wrapper

#include "Leidokos-Python.h"

#include "Kaleidoscope-MouseKeys.h"

// EXPORT_PROPERTY is an auxiliary macro that simplifies export of class
// members as Python properties.
// Here we generate accessor functions for MouseKeys's members.

#define EXPORT_PROPERTY(NAME, DESCRIPTION)                                     \
   .add_static_property(                                                       \
      #NAME,                                                                   \
      make_getter(&MouseKeys_::NAME),                                          \
      make_setter(&MouseKeys_::NAME),                                          \
      DESCRIPTION                                                              \
   )

namespace kaleidoscope {
namespace mouse_keys {

// Note: To export non-static class (struct) members, use .add_property(...)
//       instead of .add_static_property(...)

static void exportPython() {

   using namespace boost::Python;

   LEIDOKOS_PYTHON_MODULE_CONTENT(MouseKeys)

   class_<MouseKeys_>("MouseKeys")

      // Please note: Some of the members accessed below are private.
      //              For this here to work, the MouseKeys_ class must declare
      //              the below function exportPython() as
      //              friend function via the following line that must be
      //              added to MouseKey_'s class definition.
      //
      // friend void exportPython();
      //
      .EXPORT_PROPERTY(speed,
         "The mouse speed"
       )
      .EXPORT_PROPERTY(speedDelay,
         "The mouse speed delay"
       )
      .EXPORT_PROPERTY(accelSpeed,
         "The mouse acceleration speed"
       )
      .EXPORT_PROPERTY(accelDelay,
         "The mouse acceleration delay"
       )
      .EXPORT_PROPERTY(wheelSpeed,
         "The mouse wheel speed"
       )
      .EXPORT_PROPERTY(wheelDelay,
         "The mouse wheel delay"
       )
      .EXPORT_PROPERTY(mouseMoveIntent,
         "The mouse intent"
       )
      .EXPORT_PROPERTY(endTime,
         "The mouse end time"
       )
      .EXPORT_PROPERTY(accelEndTime,
         "The mouse acceleration end time"
       )
      .EXPORT_PROPERTY(wheelEndTime,
         "The mouse wheel end time"
       )

       // Export a static method.
       //
      .def("scrollWheel", &MouseKeys_::scrollWheel,
         "Scrolls the mouse wheel\n\n"
         "Args:\n"
         "   keyCode (uint8_t): The scroll wheel key code.")
         .staticmethod("scrollWheel")

      // Note: To export a non static method, just ommit the .staticmethod(...)
      //       statement.
   ;
}

LEIDOKOS_PYTHON_EXPORT(&exportPython, nullptr)

} // namespace kaleidoscope
} // namespace mouse_keys
```
