===============
uvc 调试记录
===============

uvc camera
============

需要实现的功能：

bk7236作为usb device，通过 **uvc** class 将 **h264** raw data 传输给windows，windows解析出来并播放。（也就是bk7236作为摄像头）

.. note::
    该功能基于 cherry_usb 协议栈实现，如何port cherry usb，可以看其官网文档。

调试工具：

 - Pot Player，用来播放camera的内容（打开->设备设置->摄像头->选择对应格式->打开设备）
 - Elecard StreamEye Tools，用来解析H264数据(xxx.h264)
 - ffmpeg，我只是用来从MP4文件中提取h264数据，其实它的功能很强大
 - USB packet Viewer，USB抓包工具
 - BusHound，主机收到的数据
 - usbviewer，可以用来分析UVC摄像头的描述符

推荐资源：

 - https://www.usbzh.com/article/forum-6.html
 - 几个QQ群：642693751(Cherry USB讨论群)，952873936(USB中文网技术交流群)

uvc camera 描述符相关
======================





