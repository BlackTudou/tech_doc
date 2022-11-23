==================
video
==================

video 涉及模块：
 - 8-bit CIS(CMOS Image Sensor) DVP camera interface, 720p 25fps, 1080p 12fps
 - JPEG hardware encoder/decoder, support 1080p/720p
 - DMA2D controller
 - LCD interface (16-bit parallel RGB and I8080), 720p 30fps
 - SD/SDIO
 - full-speed USB OTG (FS)
 - 8 MB SiP PSRAM

基本的硬件模块：
 - camera/sensor
 - LCD
 - sd_card/SD

 - JPEG_ENC
 - JPEG_DEC
 - DMA
 - DMA2D
 - PSRAM
 - H264
 - YUV_BUF
 - UVC/USB
 - DVP

.. toctree::
   :maxdepth: 2
   :numbered:

   camera <camera/index>
   JPEG <jpeg/index>
   yuv <yuv/index>
   LCD <lcd/index>
