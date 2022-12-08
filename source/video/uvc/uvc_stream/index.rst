==============
uvc stream
==============

uvc camera open/close
=======================

打开时，数据抓包为：

.. code-block:: text
    :linenos:

    01 0B 02 00 01 00 00 00

.. figure:: ../_static/start_stream.png
    :align: center
    :alt: Images
    :figclass: align-center

停播放时，数据抓包为：

.. code-block:: text
    :linenos:

    01 0B 00 00 01 00 00 00

.. figure:: ../_static/stop_stream.png
    :align: center
    :alt: Images
    :figclass: align-center

通过上面可以知道，打开或停止摄像头，是通过转换接口来实现的。

video stream payload Header
===============================

UVC数据传输时，每次USB传输，数据包中有一个负载数据头(Payload Header Information)，数据头后为有效的数据。其数据包格式见图：

.. figure:: ../_static/data_format.png
    :align: center
    :alt: Images
    :figclass: align-center

负载数据头为最大为12个字节，包括固定的前2字节的负载数据头和10个字节的扩展负载数据头。

.. figure:: ../_static/video_frame.png
    :align: center
    :alt: Images
    :figclass: align-center

.. figure:: ../_static/video_stream_payload_header.png
    :align: center
    :alt: Images
    :figclass: align-center