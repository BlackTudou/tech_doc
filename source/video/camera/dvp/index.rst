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