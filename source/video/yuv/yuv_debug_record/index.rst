==================
yuv 调试记录
==================

测试case
==========

测试case如下：

 - yuv mode下，数据基址为psram，完成后显示在屏幕上。（480p）
 - yuv mode下，partial 功能的测试。
 - yuv mode的高分辨率测试。（600p或720p）


测试命令
========

.. code-block:: text

    media dvp open yuv
    media lcd open

时钟配置
==========

1. 先看video模块的主时钟配置，即system里面的配置：

 - SYSTEM 0x8[30] ``clk_sel_jpeg``，选择video模块的时钟源320M/480M，一般设为1选择480M
 - SYSTEM 0x8[29:26] ``clk_div_jpeg``，video模块的分频系数，假设设为5，则video模块的时钟为80M
 - 时钟打开，需要打开这两个Bit ``jpeg_clk_en``， ``h264_clk_en``

.. note::
    关于 yuv_clk_en 这个bit，打不开开无所谓，数字没有对其做相关操作

2. 各子模块的时钟

假设video模块的主时钟为80M，那么

 - 对于H264，这80M会直接给到H264，H264模块的时钟为80M
 - 对于YUV/JPEG模块，会对80M进行2分频，即80M/2=40M

常见问题
==========

1. camera i2c 通信失败

 - 检查供电，相关跳线帽是否正常
 - 检查 MCLK，这是我们芯片供给camera的时钟，camera需要此时钟才能工作

关于如何输出MCLK，以及输出MCLK的频率，可以参考 **时钟配置** 章节。