========================
video_control_requests
========================

video_control_requests：

 - Interface Control Request
 - Unit and Terminal Control Requests

     - Camera Terminal Control Requests
     - Selector Unit Control Requests
     - Processing Unit Control Requests
     - Encoding Units
     - Extension Unit Control Requests

Interface Control Request
===========================

.. figure:: ../_static/interface_control_requests.png
    :align: center
    :alt: Images
    :figclass: align-center

The **wValue** field specifies the **Control Selector (CS)** in the high byte, and the low byte must be
set to zero.

.. figure:: ../_static/ct_control_selectors.png
    :align: center
    :alt: Images
    :figclass: align-center

Unit and Terminal Control Requests
====================================