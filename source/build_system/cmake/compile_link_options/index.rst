=============
编译链接选项
=============

编译选项
=============

---------------------
add_compile_options
---------------------

Add options to the compilation of source files.

.. note::

    1. 编译期间的选项
    2. 对所有的源文件生效 (.c .S 都会生效)
    3. 通过 ``add_compile_options`` 设置编译选项，注意这里的set后面没有引号。

--------------------------
add_compile_definitions
--------------------------

Add preprocessor definitions to the compilation of source files. 相当于 ``-DXXXXXX=1`` 选项。

---------------------------
target_compile_definitions
---------------------------

------------------------
target_compile_options
------------------------

Add compile options to a target.

These options are used when compiling the given <target>, which must have been created by a command such as ``add_executable()`` or ``add_library()`` and must not be an ALIAS target.

链接选项
===========

---------------------
add_link_options
---------------------

Add options to the **link step** for executable, shared library or module library targets in the current directory and below that are added after this command is invoked.
 - 链接这一步骤时的选项

--------------------
target_link_options
--------------------

Add options to the **link step** for an executable, shared library or module library target.

设置armino组件链接脚本

.. code-block:: cmake

    set(LINKER_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/CMSIS_5/Device/ArmChina/STAR/Source/GCC/gcc_arm.ld)
    target_link_options(${COMPONENT_LIB} INTERFACE -T ${LINKER_SCRIPT})

CMAKE_<LANG>_FLAGS
===================

CMAKE_EXE_LINKER_FLAGS //TOOD

Flags for all build types.

This is initialized for each language from environment variables:
 - CMAKE_C_FLAGS
 - CMAKE_CXX_FLAGS
 - CMAKE_ASM_FLAGS

.. note::

    1. The flags in this variable will be passed to the compiler before flags added by the add_compile_options() or target_compile_options() commands.
    2. This value is a command-line string fragment. Therefore, multiple options should be separated by spaces, and options with spaces should be quoted.


.. note::

    1. ``CMAKE_C_FLAGS`` 仅对 ``.c`` 文件生效，对 ``.s`` 不生效
    2. 编译与链接期间都会加上 ``CMAKE_C_FLAGS`` 后面的选项


如下 CMakeLists.txt 设置 ``CMAKE_C_FLAGS`` 设置为 cortex-m33 的一下选项。

.. code-block:: cmake

    # Set the minimum version of CMake that can be used
    # To find the cmake version run
    # $ cmake --version
    cmake_minimum_required(VERSION 3.5)

    # Set the project name
    project (hello_cmake C CXX ASM)

    include(./toolchain.cmake)
    set(CMAKE_TOOLCHAIN_FILE toolchain.cmake)
    set(CMAKE_VERBOSE_MAKEFILE true)

    set(MCU_C_FLAGS "-mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs")
    set(CMAKE_C_FLAGS ${MCU_C_FLAGS})

    set(SRCS startup.S main.c)
    # Add an executable
    add_executable(hello_cmake.elf ${SRCS})

下面是make时，终端的输出。

.. code-block:: shell

    [ 33%] Building ASM object CMakeFiles/hello_cmake.elf.dir/startup.S.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc    -o CMakeFiles/hello_cmake.elf.dir/startup.S.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/startup.S
    [ 66%] Building C object CMakeFiles/hello_cmake.elf.dir/main.c.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -MD -MT CMakeFiles/hello_cmake.elf.dir/main.c.o -MF CMakeFiles/hello_cmake.elf.dir/main.c.o.d -o CMakeFiles/hello_cmake.elf.dir/main.c.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/main.c
    [100%] Linking C executable hello_cmake.elf
    /usr/bin/cmake -E cmake_link_script CMakeFiles/hello_cmake.elf.dir/link.txt --verbose=1
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs CMakeFiles/hello_cmake.elf.dir/startup.S.o CMakeFiles/hello_cmake.elf.dir/main.c.o -o hello_cmake.elf
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/../lib/gcc/arm-none-eabi/9.3.1/../../../../arm-none-eabi/bin/ld: error: CMakeFiles/hello_cmake.elf.dir/startup.S.o: conflicting CPU architectures 17/2
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/../lib/gcc/arm-none-eabi/9.3.1/../../../../arm-none-eabi/bin/ld: failed to merge target specific data of file CMakeFiles/hello_cmake.elf.dir/startup.S.o
    collect2: error: ld returned 1 exit status
    make[2]: *** [CMakeFiles/hello_cmake.elf.dir/build.make:115: hello_cmake.elf] Error 1
    make[2]: Leaving directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    make[1]: *** [CMakeFiles/Makefile2:86: CMakeFiles/hello_cmake.elf.dir/all] Error 2
    make[1]: Leaving directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    make: *** [Makefile:94: all] Error 2

可以看到当我们只设置 ``CMAKE_C_FLAGS``时：
 1. startup.S 对于该文件编译时并未加上 ``-mcpu=cortex-m33+nodsp`` 的编译选项
 2. main.c 加上了 ``-mcpu=cortex-m33+nodsp`` 的编译选项
 3. Linking 时 加上了 ``-mcpu=cortex-m33+nodsp`` 的编译选项。

由此，验证上面我们说的：
 1. ``CMAKE_C_FLAGS`` 只针对 ``.c`` 文件生效，对于 ``.s`` 不生效
 2. 编译与链接阶段都会加上该选项

.. note::

    对于该例子还报了 ``conflicting CPU architectures 17/2`` 的错误，是因为编译 ``.s`` 与 ``.c`` 的跟CPU相关的选项不同。
    要想让该工程编过，还需要添加 ``set(CMAKE_ASM_FLAGS ${MCU_C_FLAGS})`` ， 设置 ``.s`` 文件的选项

如下是编译通过时，终端的输出。

.. code-block:: shell

    [ 33%] Building ASM object CMakeFiles/hello_cmake.elf.dir/startup.S.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -o CMakeFiles/hello_cmake.elf.dir/startup.S.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/startup.S
    [ 66%] Building C object CMakeFiles/hello_cmake.elf.dir/main.c.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -MD -MT CMakeFiles/hello_cmake.elf.dir/main.c.o -MF CMakeFiles/hello_cmake.elf.dir/main.c.o.d -o CMakeFiles/hello_cmake.elf.dir/main.c.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/main.c
    [100%] Linking C executable hello_cmake.elf
    /usr/bin/cmake -E cmake_link_script CMakeFiles/hello_cmake.elf.dir/link.txt --verbose=1
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs CMakeFiles/hello_cmake.elf.dir/startup.S.o CMakeFiles/hello_cmake.elf.dir/main.c.o -o hello_cmake.elf
    make[2]: Leaving directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    [100%] Built target hello_cmake.elf
    make[1]: Leaving directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    /usr/bin/cmake -E cmake_progress_start /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/CMakeFiles 0


CMAKE_C_FLAGS VS add_compile_options
======================================

----------------
CMAKE_C_FLAGS
----------------

 1. 仅针对 ``.c`` 文件生效，对 ``.s`` 不生效
 2. 编译与链接阶段都会加上该选项
 3. string 形式

--------------------
add_compile_options
--------------------

 1. 对所有的源文件生效 (.c .S 都会生效)
 2. 仅仅是编译期间的选项，链接期间不会生效
 3. 非 string 形式