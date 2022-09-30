==========
UVC 简介
==========

本栏目内容为UVC的1.5版本的中文规范，后续内容是均以此UVC1.5规范为标准（穿插着UVC其它版本规范），带你学习了和了解如何使用UVC中文协议进行UVC摄像头的开发，主要的内容包括：

 - uvc摄像头协议中的各种基础知识，如视频控制接口描述符，视频流接口描述符，特定类请求，UVC驱动中数据图像的抓取;
 - 同时在在学习过程中我们使用相关的USB/UVC摄像头软件或调试工具进行数据抓包分析。

.. note::
    只有通过大量的进行UVC通讯数据包分析，才会在UVC摄像头软件的代码开发中做到心中有码，下笔有神。

什么是UVC?
=============

UVC，全称为：USB video(device) class,是微软与另外几家设备厂商联合推出的为USB视频捕获设备定义的协议标准，目前已成为USB org标准之一。

USB协议中，除了通用的软硬件电气接口规范等，还包含了各种各样的Class协议，用来为不同的功能定义各自的标准接口和具体的总线上的数据交互格式和内容。这些Class协议的数量非常多，最常见的比如支持U盘功能的Mass Storage Class，以及通用的数据交换协议：CDC class。此外还包括Video、Audio Class, Print Class等等。正是由于这些Class协议，大大促进了USB设备的普及，比如说各个厂商生产的U盘都能通过操作系统自带的驱动程序来使用。

所以说UVC仅仅只是USB规范协议中设备类规范的其中一种，是用作USB接口的视频设备的一个统一的数据交换规范。使用 UVC 的好处 USB 在 Video这块也成为一项标准了之后，硬件在各个程序之间彼此运行会更加顺利，而且也省略了驱动程序安装这一环节，操作系统只要是 Windows XP SP2 之后的版本都可以支持 UVC，Linux系统自2.4以后的内核都支持了大量的设备驱动，其中支持UVC设备。

UVC 官方文档及下载
==================

关于UVC相关文档可以去 `USB官方网站 <http://www.usb.org/developers/docs/devclass_docs/>`_ 下载。
UVC相关文档主要有Video class 1.1 document和Video class 1.5 document，1.5为最新的规范文档在1.1上内容有所补充。
以Video class 1.5 document为例，文档压缩包内有以下文件：

:download:`/video/camera/uvc/_static/USB_Video_Class_1_5.zip`

主要以学习下列文档为主：

 - UVC 1.5 Class specification.pdf：主要描述整个规范的结构与构成
 - USB_Video_Example 1.5.pdf：主要对描述符与请求做了介绍
 - USB_Video_Transport_1.5.pdf：主要讲述数据传输的四种类型介绍
 - USB_Video_Payload_XXX：选取其中一种看即可