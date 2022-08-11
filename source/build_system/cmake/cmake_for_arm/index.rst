=================
cmake for arm
=================

工程文件目录
==============

下面使用CMake构建一个arm的工程。

.. code-block:: shell

    $tree
    .
    ├── build
    ├── CMakeLists.txt
    ├── main.c
    ├── startup.S
    └── toolchain.cmake

    0 directories, 4 files

最简单的ARM工程，编译的话只要cd到build目录下执行 ``cmake .. && make`` 就可以了。

startup.S 内容如下：

.. code-block:: c
    :linenos:

    .text
    .globl Reset_Handler
    Reset_Handler:
        ldr r0, =main
        bx r0

main.c 内容如下：

.. code-block:: c
    :linenos:

    #include <stdio.h>

    int main(int argc, char *argv[])
    {
        printf("Hello CMake!\r\n");
        return 0;
    }

设置系统和工具链
==================

toolchain.cmake 是工具链文件，可以通过 ``CMAKE_TOOLCHAIN_FILE`` 来指定，里面内容主要：

 - 设置目标系统名，目标系统处理器名
 - 设置工具链。

.. code-block:: cmake
    :linenos:

    set(CMAKE_SYSTEM_NAME Generic)
    set(CMAKE_SYSTEM_PROCESSOR arm)
    set(CMAKE_CROSSCOMPILING TRUE)

    set(CMAKE_CXX_COMPILER /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-g++)
    set(CMAKE_C_COMPILER /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc)
    set(CMAKE_ASM_COMPILER /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc)
    set(CMAKE_AR /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-ar)
    set(CMAKE_LINKER /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-ld)
    set(CMAKE_OBJCOPY /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-objcopy)
    set(CMAKE_SIZE /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-size)

cmake项目配置
=============

根目录 CMakeLists.txt 内容如下：

.. code-block:: shell
    :linenos:

    # Set the minimum version of CMake that can be used
    # To find the cmake version run
    # $ cmake --version
    cmake_minimum_required(VERSION 3.5)

    # Set the project name
    project (hello_cmake C CXX ASM)

    include(./toolchain.cmake)
    set(CMAKE_TOOLCHAIN_FILE toolchain.cmake)、

    # Enable verbose output from Makefile builds
    # show each command line as it is launched
    set(CMAKE_VERBOSE_MAKEFILE true)

    set(MCU_FLAGS -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs)
    add_compile_options(${MCU_FLAGS})
    add_link_options(${MCU_FLAGS})

    #set(MCU_C_FLAGS "-mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs")
    #set(CMAKE_C_FLAGS ${MCU_C_FLAGS})
    #set(CMAKE_ASM_FLAGS ${MCU_C_FLAGS})

    set(SRCS startup.S main.c)
    # Add an executable
    add_executable(hello_cmake.elf ${SRCS})

    set(ELF_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.elf)
    set(HEX_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.hex)
    set(BIN_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.bin)
    set(LST_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.lst)

    add_custom_command(TARGET "${PROJECT_NAME}.elf" POST_BUILD
        COMMAND ${CMAKE_OBJCOPY} -Obinary ${ELF_FILE} ${BIN_FILE}
        COMMAND ${CMAKE_OBJCOPY} -Oihex  ${ELF_FILE} ${HEX_FILE}
        COMMAND "${CMAKE_OBJDUMP}" -d -S  ${ELF_FILE} > ${LST_FILE}
        COMMENT "Generating binary image from built executable"
        DEPENDS "${PROJECT_NAME}.elf"
        VERBATIM
    )

添加编译链接选项时，可以这么添加：

.. code-block:: cmake
    :linenos:

    set(MCU_FLAGS -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs)
    add_compile_options(${MCU_FLAGS})
    add_link_options(${MCU_FLAGS})

也可以这么添加：

.. code-block:: cmake
    :linenos:

    set(MCU_C_FLAGS "-mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs")
    set(CMAKE_C_FLAGS ${MCU_C_FLAGS})
    set(CMAKE_ASM_FLAGS ${MCU_C_FLAGS})

关于编译链接选项，可以查看这一节内容 :doc:`/build_system/cmake/compile_link_options/index`

完整的make输出如下：

.. code-block:: bash

    ryan@ryan-virtual-machine:~/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build$ make
    /usr/bin/cmake -S/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake -B/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build --check-build-system CMakeFiles/Makefile.cmake 0
    /usr/bin/cmake -E cmake_progress_start /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/CMakeFiles /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build//CMakeFiles/progress.marks
    make  -f CMakeFiles/Makefile2 all
    make[1]: Entering directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    make  -f CMakeFiles/hello_cmake.elf.dir/build.make CMakeFiles/hello_cmake.elf.dir/depend
    make[2]: Entering directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    cd /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build && /usr/bin/cmake -E cmake_depends "Unix Makefiles" /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/CMakeFiles/hello_cmake.elf.dir/DependInfo.cmake --color=
    Scanning dependencies of target hello_cmake.elf
    make[2]: Leaving directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    make  -f CMakeFiles/hello_cmake.elf.dir/build.make CMakeFiles/hello_cmake.elf.dir/build
    make[2]: Entering directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    [ 33%] Building ASM object CMakeFiles/hello_cmake.elf.dir/startup.S.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -o CMakeFiles/hello_cmake.elf.dir/startup.S.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/startup.S
    [ 66%] Building C object CMakeFiles/hello_cmake.elf.dir/main.c.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -MD -MT CMakeFiles/hello_cmake.elf.dir/main.c.o -MF CMakeFiles/hello_cmake.elf.dir/main.c.o.d -o CMakeFiles/hello_cmake.elf.dir/main.c.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/main.c
    [100%] Linking C executable hello_cmake.elf
    /usr/bin/cmake -E cmake_link_script CMakeFiles/hello_cmake.elf.dir/link.txt --verbose=1
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc -mcpu=cortex-m33+nodsp -march=armv8-m.main -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs CMakeFiles/hello_cmake.elf.dir/startup.S.o CMakeFiles/hello_cmake.elf.dir/main.c.o -o hello_cmake.elf
    Generating binary image from built executable
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-objcopy -Obinary /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/hello_cmake.elf /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/hello_cmake.bin
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-objcopy -Oihex /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/hello_cmake.elf /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/hello_cmake.hex
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-objdump -d -S /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/hello_cmake.elf > /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/hello_cmake.lst
    make[2]: Leaving directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    [100%] Built target hello_cmake.elf
    make[1]: Leaving directory '/home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build'
    /usr/bin/cmake -E cmake_progress_start /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/build/CMakeFiles 0

完整的工程目录如下：

:download:`/build_system/cmake/cmake_for_arm/hello-cmake.rar`