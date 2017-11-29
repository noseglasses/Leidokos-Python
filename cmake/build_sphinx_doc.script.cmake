set(ENV{PYTHONPATH} "${kaleidoscope_module_path}:${kaleidoscope_testing_module_path}:$ENV{PYTHONPATH}")

set(kaleidoscope_doc_file "${sphinx_build_dir}/html/modules.html")
execute_process(
   COMMAND "${sphinx_executable}" -b html "${sphinx_configuration_dir}/source" "${sphinx_build_dir}"
)