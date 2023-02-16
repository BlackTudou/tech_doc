===================
简单的链接脚本命令
===================

设置入口点（entry）
====================

处理文件的命令
=====================

-------------------
INCLUDE filename
-------------------

处理目标文件格式的命令
==========================


其他链接脚本命令（Other linker script commands）
=====================================================


In a link script, why .bss (NOLOAD) ?

Using the "NOLOAD" attribute for the ".bss" section reduces the size of the executable file, since it does not need to store the zero-initialized data.