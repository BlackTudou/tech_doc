=====
usb
=====

相关资源
============

参考资料：

 - `USB官方文档 <https://www.usb.org/documents>`_
 - `CherryUSB文档 <https://cherryusb.readthedocs.io/zh_CN/latest/>`_
 - `usb-20-specification <https://www.usb.org/document-library/usb-20-specification>`_
 - <<圈圈教你玩USB>>
 - 简书 jianshu_kevin@126.com 的文章

     - `USB协议 (一) <https://www.jianshu.com/p/3afc1eb5bd32>`_
     - `USB协议 (二) <https://www.jianshu.com/p/cf8e7df5ff09>`_
     - `USB协议 (三) <https://www.jianshu.com/p/2a6e22194cd3>`_

armino usb 使用
==================

----------
宏配置
----------

1. 以7236为例：

middleware\soc\bk7236\bk7236.defconfig

properties\soc\bk7236\bk7236.defconfig

2. 找到USB相关宏定义

CONFIG_USB  开关宏，决定是否使用USB  总开关

CONFIG_USB_HOST

CONFIG_USB_DEVICE

设备作为host 或device 宏开关

CONFIG_USB_MSD
CONFIG_USB_HID
CONFIG_USB_CCD
CONFIG_USB_UVC
使用USB的什么功能使用


3、例子：usb打开   device模式   msd功能
#
# USB configuration
#
CONFIG_USB=y

#
# USB
#
# CONFIG_USB_HOST is not set
CONFIG_USB_DEVICE=y
# CONFIG_USB1_PORT is not set
CONFIG_TASK_USB_PRIO=5
CONFIG_USB_MSD=y
# CONFIG_USB_HID is not set
# CONFIG_USB_CCD is not set
# CONFIG_USB_UVC is not set
# CONFIG_USB_CHARGE is not set
# end of USB configuration

----------
cli 测试
----------

cli_usb.c