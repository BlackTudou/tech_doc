============
beken jpeg
============

概述
======

通过 dvp camera 过来的数据，会有三种处理方式，对应芯片里面的硬件模块：
  - yuv_buf
  - jpeg_enc
  - h264

这些模块依赖于 sensor 输出的 **PCLK** (一般是20M这个级别)。

---------
yuv mode
---------

sensor 过来的数据(yuv/rgb data)，倒手一波，放在 ``em_base_addr`` 里面，因为数据量比较大，因此通常是 ``PSRAM`` 的地址(0x60000000)。

----------
jpeg mode
----------

sensor 过来的数据，进行 JPEG 压缩，因此需要一个地方来处理数据，这个就是 ``em_base_addr`` 设置的地方，通常是 ``share_memory`` ，因为需要速度够快。

压缩完成后的数据放在 ``jpeg_enc`` 的 ``rx_fifo_data`` 里面，因此读这个fifo就可以得到压缩处理后的数据。通常通过DMA来搬。

JPEG 模式
===========

工作正常的指标：

 - byte_count_pfrm 一直变化
 - rx_fifo_data 一直变化
 - sof , eof 这两个中断都一直产生

JPEG 调试记录
=====================

1. JPEG 模块是否工作正常主要关注：
   - REG_0x7 byte_count_pfrm(bit[0:31]): the byte number of every frame，JPEG 正常工作起来后这个值会不停的变化
   - REG_0x5 rx_fifo_data(bit[0:31]): jpeg encoder output data, JPEG 正常工作起来后这个值也会不停的变化

2. JPEG 配置
   - REG_0x4 eof_offset=0x20
   - REG_0xC
   - REG_0xD bit[1] video_byte_reverse=1
   - REG_0xD bit[8:15] x_pixel=40，bit[24:31] y_pixel=60 (320*480)

调试中遇到的问题
===================

-----------------------------------------
byte_count_pfrm 一直是0
-----------------------------------------

JPEG 没工作起来
 - jpeg_en 使能
 - jpeg 分辨率跟摄像头分辨率配置一致
 - camera init 后延时一段时间再去打开GPIO 的VSYNC,HSYNC
 - clock_gate_bypass 打开
