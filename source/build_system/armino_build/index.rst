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


cd .