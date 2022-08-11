==========
cmake
==========

.. toctree::
   :maxdepth: 2
   :numbered:

    hello cmake <hello_cmake/index>
    头文件/源文件设置 <header_source_files/index>
    构建和链接静态库 <static_library/index>
    编译链接选项 <compile_link_options/index>


Compiler Option
=================

CMake exposes options to control the programs used to compile and link your code. These programs include:
 - CMAKE_C_COMPILER - The program used to compile c code.
 - CMAKE_CXX_COMPILER - The program used to compile c++ code.
 - CMAKE_LINKER - The program used to link your binary.

Compiler Flags
=================

CMake supports setting compile flags in a number of different ways:

 - using target_compile_definitions() function
 - using the CMAKE_C_FLAGS and CMAKE_CXX_FLAGS variables.

---------------------------
Set Per-Target C++ Flags
---------------------------

.. code-block:: cmake

    target_compile_definitions(cmake_examples_compile_flags
        PRIVATE EX3
    )

    target_compile_options()

``target_compile_definitions`` This will cause the compiler to add the definition -DEX3 when compiling the target.

---------------------------
Set Set Default C++ Flags
---------------------------

The default CMAKE_CXX_FLAGS is either empty or contains the appropriate flags for the build type.

To set additional default compile flags you can add the following to your top level CMakeLists.txt

 - CMAKE_CXX_FLAGS - Setting C++ compiler flags
 - CMAKE_C_FLAGS - Setting C compiler flags
 - CMAKE_EXE_LINKER_FLAGS - Setting linker flags


设置编译选项
================

---------------------
add_compile_options
---------------------

通过 ``add_compile_options`` 设置编译选项，注意这里的set后面没有引号。

.. code-block:: cmake

    set(MCU_FLAGS -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard)
    add_compile_options(${MCU_FLAGS})


-----------------------------------------------
CMAKE_CXX_FLAGS/CMAKE_C_FLAGS/CMAKE_ASM_FLAGS
-----------------------------------------------

CMAKE_C_FLAGS
CMAKE_ASM_FLAGS

---------------------------
target_compile_options
---------------------------

 Add compile options to a target


使用CMAKE构建嵌入式工程
==========================

问题集锦
==================

conflicting CPU architectures 2/17
-----------------------------------

完整的错误信息如下所示：

.. code-block:: shell

    arm-none-eabi/bin/ld: error: CMakeFiles/hello_cmake.elf.dir/startup.S.o: conflicting CPU architectures 2/17

问题分析：
既然是冲突，那肯定是A跟B不一样导致的冲突：
 - 编译选项冲突，是不是有的源文件编译使用的是 ``-mcpu=cortex-m33+nodsp`` ，有的源文件使用的是

root cause:
    编译选项与链接选项不一致