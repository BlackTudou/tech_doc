==============
video basics
==============

视频录制原理
==============

.. figure:: _static/video_record.png
    :align: center
    :alt: Images
    :figclass: align-center

视频播放原理
==============

.. figure:: _static/video_player.png
    :align: center
    :alt: Images
    :figclass: align-center

图像表示
=========

------------------
图像表示 - RGB格式
------------------

RGB指的是R(red)红色、G（green）绿色、B（blue）蓝色，三种颜色。
目前来说，所有的颜色都可以用这三种颜色配出来,RGB各有256级亮度，用数字表示为从0、1、2…直到255,最多可以表示256×256×256=16777216种色彩。

.. figure:: _static/rgb.png
    :align: center
    :alt: Images
    :figclass: align-center

对于一幅图像，一般使用整数表示方法来进行描述，

 - RGB_888(3 bytes)
 - RGB_565(2 bytes)

比如计算一张的RGB_888图像的大小，可采用如下方式：

1280×720 * 3 = 2.637 MB，4分钟就达到了2.637x25x60x4=15G的容量。

假如是一部90分钟的电影，每秒25帧，则一部电影为

2.637MB*90分钟*60秒*25FPS= 347.651GB

------------------
图像表示 - YUV格式
------------------

用途：主要用于视频信号的压缩、传输和存储，和向后相容老式黑白电视。

其中“Y”表示明亮度（Luminance或Luma）， **也称灰阶值**；

“U”和“V”表示的则是色度（Chrominance或Chroma）

作用是描述影像色彩及饱和度，用于指定像素的颜色。

.. figure:: _static/yuv.png
    :align: center
    :alt: Images
    :figclass: align-center

YUV格式有两大类：

 - planar
 - packed

对于 **planar** 的YUV格式，先连续存储所有像素点的Y，紧接着存储所有像素点的U，随后是所有像素点的V。

.. figure:: _static/planar_format.png
    :align: center
    :alt: Images
    :figclass: align-center

    YUV444 planar格式

对于 **packed** 的YUV格式，每个像素点的Y,U,V是连续交替存储的。

.. figure:: _static/packet_format.png
    :align: center
    :alt: Images
    :figclass: align-center

    YUV444 packet格式

