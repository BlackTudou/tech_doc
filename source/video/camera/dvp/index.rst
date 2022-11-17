=====
dvp
=====

DVP (digital video port)

CIS DVP 接口，支持720P 25fps，1080p 12fps

Supported sensors could be but not limited to OV7676, OV7670, GC0308, GC0309, GC0329 and PAS6329.
The sensor YUV input will be directly fed to the hardware JPEG encoder, and the JPEG encoder output will be write to data
memory directly by a dedicated DMA channel.
The YUV signal format could be YUYV, UYVY, YYUV and UVYY. HSYNC and VSYNC level could be set
independently.

bk7236 芯片配置
================

---------
时钟相关
---------

1. yuv, jpeg, h264 时钟都要打开，即 system 里面的 clk_en 都要设置为1
2. 时钟选择：system_reg8[30] 选择320M/480M，system_reg[29:26] 配置分频系数

     假设选择 480M，分频系数=3，那么
       - H264的时钟就是480M/4=120M，
       - JPEG,YUV 的时钟源是 H264 的时钟源再2分频，即JPEG,YUV 的时钟源为60M
3. mclk 配置：在yuv_buf_reg0x4[11:10]配分频系数，在60M(步骤2配的yuv_buf的时钟源)的基础上在分频

Q&A
======

1. GC0328C 写 slave_address(0x42)，camera不回ACK。

   camera正常工作需要电源跟MCLK，检查这两个地方是否正常。

   - AVDD28：模拟供电电源 2.8V
   - IOVDD：I/O 电源 2.8V
   - DVDD：数字供电电源 1.8V