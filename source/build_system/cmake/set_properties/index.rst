================
set properties
================

set_source_files_properties
============================

Source files can have properties that affect how they are built.
Sets properties associated with source files using a key/value paired list.

.. code-block:: cmake

    set_source_files_properties("${CMAKE_CURRENT_LIST_DIR}/port.c" PROPERTIES COMPILE_FLAGS "-marm")
    # 设置这些源文件的优化级别调到 -O2
    set_source_files_properties(${_source} PROPERTIES COMPILE_FLAGS -O2)

set_target_properties
=======================

Targets can have properties that affect how they are built.