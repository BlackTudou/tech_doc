=========
FAQ
=========

conflicting CPU architectures 2/17
=====================================

-----------
问题现象
-----------

完整的错误信息如下所示：

.. code-block:: bash

    arm-none-eabi/bin/ld: error: CMakeFiles/hello_cmake.elf.dir/startup.S.o: conflicting CPU architectures 2/17

-----------
问题分析
-----------

既然是冲突，那肯定是A跟B不一样导致的冲突：

 - 编译选项冲突，是不是有的源文件编译使用的是 ``-mcpu=cortex-m33+nodsp`` ，有的源文件使用的是 ``arm9``
 - 编译与链接阶段的CPU相关选项不同而引起的冲突
 - .s 跟 .c 文件编译选项不同引起的冲突。

我们现将 ``set(CMAKE_VERBOSE_MAKEFILE true)`` ，这样可以看到Makefile的每一条命令。

.. code-block:: bash

    [ 33%] Building ASM object CMakeFiles/hello_cmake.elf.dir/startup.S.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -o CMakeFiles/hello_cmake.elf.dir/startup.S.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/startup.S
    [ 66%] Building C object CMakeFiles/hello_cmake.elf.dir/main.c.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -MD -MT CMakeFiles/hello_cmake.elf.dir/main.c.o -MF CMakeFiles/hello_cmake.elf.dir/main.c.o.d -o CMakeFiles/hello_cmake.elf.dir/main.c.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/main.c
    [100%] Linking C executable hello_cmake.elf
    /usr/bin/cmake -E cmake_link_script CMakeFiles/hello_cmake.elf.dir/link.txt --verbose=1
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc CMakeFiles/hello_cmake.elf.dir/startup.S.o CMakeFiles/hello_cmake.elf.dir/main.c.o -o hello_cmake.elf
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/../lib/gcc/arm-none-eabi/9.3.1/../../../../arm-none-eabi/bin/ld: error: CMakeFiles/hello_cmake.elf.dir/startup.S.o: conflicting CPU architectures 2/17
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/../lib/gcc/arm-none-eabi/9.3.1/../../../../arm-none-eabi/bin/ld: failed to merge target specific data of file CMakeFiles/hello_cmake.elf.dir/startup.S.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/../lib/gcc/arm-none-eabi/9.3.1/../../../../arm-none-eabi/bin/ld: error: CMakeFiles/hello_cmake.elf.dir/main.c.o uses VFP register arguments, hello_cmake.elf does not

跟CPU架构相关的关键配置选项： ``-mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard`` ，
可以看到编译 main.c 与 startup.S 都有该选项，但是链接时 ``arm-none-eabi-gcc CMakeFiles/hello_cmake.elf.dir/startup.S.o CMakeFiles/hello_cmake.elf.dir/main.c.o -o hello_cmake.elf`` 未看到CPU相关的选项。
可以推断是 **编译** 跟 **链接** 时的CPU选项不同导致。

root cause:
    编译选项与链接选项不一致

-----------
解决方案
-----------

可以看到编译选项是通过 ``add_compile_options`` 添加的

.. code-block:: cmake

    set(MCU_FLAGS -mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs)
    add_compile_options(${MCU_FLAGS})

因此，我们可以在后面添加 ``add_link_options(${MCU_FLAGS})`` 可以解决。

.. code-block:: cmake

    set(MCU_FLAGS -mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs)
    add_compile_options(${MCU_FLAGS})
    add_compile_options(${MCU_FLAGS})


还有一种方案可以 可以通过 ``CMAKE_C_FLAGS`` 来设置，它会作用于编译链接阶段都会生效。

.. code-block:: cmake

    set(MCU_C_FLAGS "-mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs")
    set(CMAKE_C_FLAGS ${MCU_C_FLAGS})

关于编译链接选项，可以查看这一节内容 :doc:`/build_system/cmake/compile_link_options/index`

修改后，可以看到如下编译链接细节，编译跟链接跟CPU相关的选项都一致了，编译通过。

.. code-block:: bash

    [ 33%] Building ASM object CMakeFiles/hello_cmake.elf.dir/startup.S.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -o CMakeFiles/hello_cmake.elf.dir/startup.S.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/startup.S
    [ 66%] Building C object CMakeFiles/hello_cmake.elf.dir/main.c.o
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc   -mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs -MD -MT CMakeFiles/hello_cmake.elf.dir/main.c.o -MF CMakeFiles/hello_cmake.elf.dir/main.c.o.d -o CMakeFiles/hello_cmake.elf.dir/main.c.o -c /home/ryan/work/cmake_doc/cmake-examples/01-basic/A-hello-cmake/main.c
    [100%] Linking C executable hello_cmake.elf
    /usr/bin/cmake -E cmake_link_script CMakeFiles/hello_cmake.elf.dir/link.txt --verbose=1
    /opt/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc -mcpu=cortex-m33+nodsp -mfpu=fpv5-sp-d16 -mfloat-abi=hard -specs=nosys.specs CMakeFiles/hello_cmake.elf.dir/startup.S.o CMakeFiles/hello_cmake.elf.dir/main.c.o -o hello_cmake.elf
