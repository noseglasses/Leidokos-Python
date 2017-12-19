#  -*- mode: cmake -*-
# Kaleidoscope-Python -- Wraps Kaleidoscope modules' c++
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

# Generate API documentation with sphinx
#
set(KALEIDOSCOPE_PYTHON_GENERATE_API_DOC FALSE CACHE BOOL 
   "Enable creation of the python API documentation. This requires Sphinx to be installed")
   
if(KALEIDOSCOPE_PYTHON_GENERATE_API_DOC)

   find_program(SPHINX_EXECUTABLE NAMES sphinx-build
      HINTS
      $ENV{SPHINX_DIR}
      PATH_SUFFIXES bin
      DOC "Sphinx documentation generator"
   )
   
   include(FindPackageHandleStandardArgs)
   
   find_package_handle_standard_args(Sphinx DEFAULT_MSG
      SPHINX_EXECUTABLE
   )
   
   mark_as_advanced(SPHINX_EXECUTABLE)
   
   if(NOT EXISTS "${SPHINX_EXECUTABLE}")
      message("Please specify a valid SPHINX_EXECUTABLE")
   endif()
   
   find_program(SPHINX_APIDOC_EXECUTABLE NAMES sphinx-apidoc
      HINTS
      $ENV{SPHINX_DIR}
      PATH_SUFFIXES bin
      DOC "Sphinx apidoc documentation generator"
   )
   
   include(FindPackageHandleStandardArgs)
   
   find_package_handle_standard_args(Sphinx_Apidoc DEFAULT_MSG
      SPHINX_APIDOC_EXECUTABLE
   )
   
   mark_as_advanced(SPHINX_APIDOC_EXECUTABLE)
   
   if(NOT EXISTS "${SPHINX_APIDOC_EXECUTABLE}")
      message("Please specify a valid SPHINX_APIDOC_EXECUTABLE")
   endif()
   
   set(python_sources
      "${CMAKE_SOURCE_DIR}/python/kaleidoscope.py"
   )
   
   set(sphinx_configuration_dir "${CMAKE_BINARY_DIR}/doc/sphinx")

   # Copy the Sphinx configuration to the target location
   #
   set(sphinx_conf_file_source_location "${CMAKE_SOURCE_DIR}/doc/sphinx/source/conf.py.in")
   set(sphinx_conf_file_target_location "${sphinx_configuration_dir}/source/conf.py")
   if(NOT EXISTS "${sphinx_conf_file_target_location}")
      file(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/doc/sphinx/source")
      configure_file("${sphinx_conf_file_source_location}" "${sphinx_conf_file_target_location}")
      file(GLOB rst_files "${CMAKE_SOURCE_DIR}/doc/sphinx/source/*.rst")
      foreach(rst_file ${rst_files})
         execute_process(
            COMMAND ${CMAKE_COMMAND} -E copy "${rst_file}" "${sphinx_configuration_dir}/source"
         )
      endforeach()
   endif()
   
   # Auto-generate Sphinx input from python sources
   #
#    set(kaleidoscope_testing_target_location "${sphinx_configuration_dir}/source/kaleidoscope.rst")
#    add_custom_command(
#       OUTPUT "${kaleidoscope_testing_target_location}"
#       COMMAND "${SPHINX_APIDOC_EXECUTABLE}" -f --private -o "${sphinx_configuration_dir}/source" "${CMAKE_SOURCE_DIR}/python"
#       DEPENDS ${python_sources}
#       COMMENT "Generating Sphinx input files"
#    )
#    add_custom_target(generate_sphinx_input_files DEPENDS "${kaleidoscope_testing_target_location}")
#    add_dependencies(generate_sphinx_input_files copy_sphinx_configuration)
   
   # Generate documentation
   
   
   set(sphinx_build_dir "${CMAKE_BINARY_DIR}/doc/kaleidoscope/API")
   set(kaleidoscope_doc_file "${sphinx_build_dir}/modules.html")
   add_custom_command(
      OUTPUT "${kaleidoscope_doc_file}"
      COMMAND "${CMAKE_COMMAND}" 
         "-Dkaleidoscope_module_path=${CMAKE_BINARY_DIR}"
         "-Dkaleidoscope_testing_module_path=${CMAKE_SOURCE_DIR}/python"
         "-Dsphinx_build_dir=${sphinx_build_dir}"
         "-Dsphinx_executable=${SPHINX_EXECUTABLE}"
         "-Dsphinx_configuration_dir=${sphinx_configuration_dir}"
         -P "${CMAKE_SOURCE_DIR}/cmake/build_sphinx_doc.script.cmake"
      DEPENDS "${kaleidoscope_firmware_target}"
      COMMENT "Generating Sphinx python documentation"
   )
   add_custom_target(doc DEPENDS "${kaleidoscope_doc_file}")
#    add_dependencies(doc generate_sphinx_input_files)
   add_dependencies(doc "${kaleidoscope_firmware_target}")
   
   # The .nojekyll file is necessary to prevent jekyll from being used when 
   # publishing the html stuff
   #
   file(WRITE "${sphinx_build_dir}/.nojekyll" "")
endif()