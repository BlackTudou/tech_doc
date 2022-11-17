==============
armino build
==============

armino 编译
==============

-----------------------------
macro(project project_name)
-----------------------------

---------------------------------------
macro(armino_build_process target)
---------------------------------------

--------------------------
armino_build_executable
--------------------------


.. code-block:: cmake
    :linenos:

    add_custom_command(OUTPUT "${bin_dir}/bin_tmp"
        COMMAND "${armino_objcopy}" -O binary "${bin_dir}/${bin}" "${bin_dir}/${bin_name}.bin"
        COMMAND "${armino_readelf}" -a -h -l -S -g -s "${bin_dir}/${bin}" > "${bin_dir}/${bin_name}.txt"
        COMMAND "${armino_nm}" -n -l -C -a -A -g "${bin_dir}/${bin}" > "${bin_dir}/${bin_name}.nm"
        COMMAND "${armino_objdump}" -d "${bin_dir}/${bin}" > "${bin_dir}/${bin_name}.lst"
        COMMAND python "${armino_pack}" -n "all-${bin_name}.bin" -f "${bin_name}.bin" -c "${ARMINO_SOC}"
        DEPENDS ${bin}
        VERBATIM
        WORKING_DIRECTORY ${bin_dir}
        COMMENT "Generating binary image from built executable"
    )

armino 工具链升级
======================

将 ``bk7236`` 工具链升级到 ``gcc-arm-none-eabi-9-2020-q2-update-x86_64-linux.tar.bz2``

 - 下载工具链，默认解压放到/opt/目录下 https://developer.arm.com/downloads/-/gnu-rm
 - 修改工具链路径配置项

.. code-block:: c
    :linenos:

    middleware/soc/bk7236/bk7236.defconfig
    properties/soc/bk7236/bk7236.defconfig

    CONFIG_TOOLCHAIN_PATH="/opt/gcc-arm-none-eabi-9-2020-q2-update/bin"

armino 添加 arch cm33
=========================

------------
编译选项
------------

详细参考：https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html

修改编译选项，以支持 ``CM33``

1. ``-mcpu=name``    ``-mcpu=cortex-m33+nodsp``
2. ``-mthumb-interwork``：Generate code that supports calling between the ARM and Thumb instruction sets.Without this option, on pre-v5 architectures, the two instruction sets cannot be reliably used inside one program.
3. ``-mlittle-endian``
4. ``-mcmse``：Generate secure code as per the "ARMv8-M Security Extensions

----------
问题记录
----------

1. 编译出来的 app.bin 为 0 byte

   汇编程序的缺省入口是 start标号，用户也可以在连接脚本文件中用ENTRY标志指明其它入口点（见上文关于连接脚本的说明）。

   检查 链接脚本 bk7236_bsp.ld， ``ENTRY(_vector_start);``

在 armino 的链接脚本中使用宏定义
====================================

------------------------------
在链接脚本使用宏定义
------------------------------

问题：需要在ld script中使用类似C语言的define等宏定义来做一些判断和替换。如果不做任何处理，直接在ld文件中 ``#include "xxxx.h"`` ,会报如下错误：

.. code-block:: shell

    ignoring invalid character `#' in expression
    syntax error

解决思路：

.c中为什么能用define等宏，这个是在预处理阶段完成的，因此基本思路是用gcc的预处理将ld文件当做.c文件来处理，实现宏替换。参考命令如下：

.. code-block:: shell

    arm-none-eabi-gcc -E -P - < bk7236_bsp.ld -o bk7236_bsp_out.ld -I ../../../include/ -I ../../../build/app/bk7236/config/

-E Preprocess only; do not compile, assemble or link

-P

----------------------------
更改armino的链接脚本
----------------------------

默认使用的是bk7236_bsp.ld，想换成bk7236_out.ld，因为链接脚本最终是通过-T选项链接上的，因此grep "-T" 一下，然后顺藤摸瓜往上找下。

   原先在 middleware/soc/bk7236/CMakeLists.txt 里面的 target_linker_script_judge() 选择链接脚本，
   最终是调用 ``target_linker_script`` 来实现，通过如下代码可以看到最终是调用 ``target_link_libraries("${target}" "${deptype}" "-T ${scriptname}")``。
   通过 ``-T`` 选项选择链接脚本。

.. code-block:: cmake
    :linenos:

    function(target_linker_script target deptype scriptfiles)
        cmake_parse_arguments(_ "" "PROCESS" "" ${ARGN})
        foreach(scriptfile ${scriptfiles})
            get_filename_component(abs_script "${scriptfile}" ABSOLUTE)
            LOGI("Adding linker script ${abs_script}")

            if(__PROCESS)
                get_filename_component(output "${__PROCESS}" ABSOLUTE)
                __ldgen_process_template(${abs_script} ${output})
                set(abs_script ${output})
            endif()

            get_filename_component(search_dir "${abs_script}" DIRECTORY)
            get_filename_component(scriptname "${abs_script}" NAME)

            if(deptype STREQUAL INTERFACE OR deptype STREQUAL PUBLIC)
                get_target_property(link_libraries "${target}" INTERFACE_LINK_LIBRARIES)
            else()
                get_target_property(link_libraries "${target}" LINK_LIBRARIES)
            endif()

            list(FIND "${link_libraries}" "-L ${search_dir}" found_search_dir)
            if(found_search_dir EQUAL "-1")  # not already added as a search path
                target_link_libraries("${target}" "${deptype}" "-L ${search_dir}")
            endif()

            target_link_libraries("${target}" "${deptype}" "-T ${scriptname}")

            # Note: In BEKEN-ARMINO, most targets are libraries and libary LINK_DEPENDS don't propagate to
            # executable(s) the library is linked to. Attach manually to executable once it is known.
            #
            # Property INTERFACE_LINK_DEPENDS is available in CMake 3.13 which should propagate link
            # dependencies.
            if(NOT __PROCESS)
                armino_build_set_property(__LINK_DEPENDS ${abs_script} APPEND)
            endif()
        endforeach()
    endfunction()

最终middleware/soc/bk7236/CMakeLists.txt修改如下：

.. code-block:: cmake
    :linenos:

    set(LD_DIR ${CMAKE_CURRENT_SOURCE_DIR})

    add_custom_command(
        OUTPUT ${target}_out.ld
        COMMAND "${CMAKE_C_COMPILER}" -P -x c -E - < ${LD_DIR}/${target}_bsp.ld -o ${target}_out.ld -I ${armino_path}/include/ -I ${config_dir}
        MAIN_DEPENDENCY ${LD_DIR}/${target}.ld ${sdkconfig_header}
        COMMENT "Generating linker script..."
        VERBATIM)

    add_custom_target(${target}_linker_script DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${target}_out.ld)
    add_dependencies(${COMPONENT_LIB} ${target}_linker_script)

    target_linker_script(${COMPONENT_LIB} INTERFACE "${CMAKE_CURRENT_BINARY_DIR}/${target}_out.ld")

armino 配置
===========

1. 其中 project 下是特定项目的配置，例如，海尔/涂鸦使用了 armino，则他们就在 project 下定制他们自己的配置。 如果海尔一个项目 hai_iot 同时使用了 bk7256/bk7236，那么就通过 project/config/bk7256.config 与 project/config/bk7236.config 来区分，而通用的配置就放在 project/config/common.config 中，客户仅能修改 project 下的配置。。。当然，咱们也可以针对典型项目提供一组默认配置，如针对 audio 提供一组默认配置。

2. middleware/soc/bk7236.defconfig 或者  properties/soc/bk7236.defconfig 是 sdk 级 soc 的配置差异化，即对于 beken 内部团队而言，用它来差异化不同 soc 的配置，为客户提供一组默认值。

3. 组件级则是定义配置，并给出一个默认初始配置。一个配置项只有在组件中定义之后才变成可配置。

4. Kconfig 主要定义组件级的编译配置，其他打包，flash 相关，校准等配置通常不放在 Kconfig 中，而是独立定义。