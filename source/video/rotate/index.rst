=========
rotate
=========

模块简介
============

旋转模块（Rotate module）主要功能是将储存在 memory 的 yuv422 图像，旋转成 rgb565 格式的图像，完成后储存在另一块 memory 中。

模块共有三种工作模式：

 1. 顺时针旋转模式
 2. 逆时针旋转模式
 3. 不旋转只进行格式转换(yuv422转为RGB565)

旋转过程中将整张图像分解为多张小图像（Rblock），按 Rblock 从左至右，从上之下全部旋转完成。

运行流程
===========

Rotate Module 进行旋转操作时，并非是直接对整幅图像图像直接进行旋转，而是将图像分解为多个低像素的 Rblock（大小由用户控制）。

对每一个 Rblock 进行旋转，写入内部的 memory 中，旋转完成后直接将 Rblock 写入外部的存储区。

遵循从左至右，从上之下的顺序，对每一个 Rblock 旋转写入， 直到整个图像完成。

使用示例
==========

将 1280*720 大小的图像进行顺时针旋转

1. 首先计算 Rblock 大小和 Rblock 的个数

内部的存储 memory 为 32bit*2400=9600byte，一个pixel 2byte，所以最大单个 Rblock 为 **4800 个 pixel**。

设置 Rblock 为 80x60，即 Rblock行像素=80，Rblock列像素=60

Rblock_cnt 为 (1280*720)/(80*60) = 16*12 = 192

.. note::

    block 的 x_pixel 必须能被 图像的 x_pixel 整除。如 1280x720 的图像，Rblock需设置为80x60，而不能设置为60x80。(1280/60=21.3)

2. 配置 Rotate module 的时钟，该时钟与 core clk 同源，更改该时钟更改 core_clk。

3. 配中断，选择要使用的中断，并对中断进行使能

 - 旋转完成中断
 - 旋转的水位中断，该中断指示旋转过程到达用户设置的水位位置
 - 旋转设置错误中断

4. 选择模式

操作 rotate_anticlock 和 rotate_bps 寄存器

5. 配置原图像的分辨率

pic_line_pixel 和 pic_clum_pixel

6. 原始图像和目标图像的地址设置。

rotate_rd_base_addr 和 rotate_wr_base_addr

7. 如果要在旋转过程中进行操作，可以对 wtmk 进行设置。

wtmk_clum_pixel 设置为96，即旋转到一半会产生旋转的水位中断，方便软件使用 ping pong buffer

8. 设置旋转使能。 rotate_ena。

9. 旋转完成，进入中断。旋转使能会在完成后自动关闭（与中断无关系）。

API 使用示例
==============

.. code-block:: c

    bk_rott_driver_init();
    bk_rott_int_enable(ROTATE_COMPLETE_INT | ROTATE_CFG_ERR_INT | ROTATE_WATERMARK_INT, 1);
    bk_rott_wartermark_block_config(96);
    bk_rott_mode_config(ROTT_ONLY_YUV2RGB565);
    bk_rott_input_data_format(PIXEL_FMT_VUYY);
    bk_rott_block_rotate_config(1280, 720, 80, 60, 192);
    bk_rott_wr_addr_config(60200000, 60400000);
    bk_rott_enable(1);