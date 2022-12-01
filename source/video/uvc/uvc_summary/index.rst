==============
uvc summary
==============

uvc 拓扑结构
================

This specification describes the following types of standard Units and Terminals that are
considered adequate to represent most video functions available today and in the near future:

 - Input Terminal(IT)
 - Output Terminal(OT)
 - Selector Unit(SU)
 - Processing Unit(PU)
 - Encoding Unit(EU)
 - Extension Unit(XU)

Also, there are certain special Terminals that extend the functionality of the basic Input and
Output Terminals. These special Terminals support additional Terminal Descriptor fields and
Requests that are specific to the extended features these Terminals provide. These include:

 - Media Transport Terminal
 - Camera Terminal(CT)

UVC摄像头设备拓扑结构
==========================

下面以一个UVC摄像头设备为例展现其拓扑结构的示例图如下：

.. figure:: ../_static/uvc_camera.png
    :align: center
    :alt: Images
    :figclass: align-center

从Sensor和另一个复合视频设备得到的数据流由IT和CT输入，经过SU选择送到PU处理，再由OT绑定到指定的USB端点。

同时从上面的拓扑结构图可以看出，左半部分框架组成了UVC中的 **VC接口部分** ，右半部分框架组成了 **VS接口部分**。