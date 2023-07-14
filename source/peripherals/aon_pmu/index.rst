===========
aon pmu
===========

关于 PMU_REG0 的使用
======================

--------
简介
--------

PMU_REG0 在系统中有两份，

 - 一份在0.9V域
 - 一份在3V域

或者说一份在模拟，一份在数字，

3V的这一份不会掉电，aon_wdt 重启也不会对3V的这一份进行复位，因此，可以用3V的 REG0 来保存重启的类型信息(wdt重启，deep sleep重启等)

关于3V域下的REG0：

首先，3V域下的 ``PMU_REG0`` 被映射到 ``PMU_REG7B``，

其次， ``PMU_REG7B`` 的写操作不能直接操作 ``PMU_REG7B``，需要通过 ``PMU_REG25`` 将 ``PMU_REG0`` 的值传递给 ``PMU_REG7B``。

--------------
如何使用
--------------

关于 3V 域下 PMU_REG0 的写操作：

 - 设置PMU_REG0
 - 设置PMU_REG25 两个特殊值，这个值数字同事给的，具体啥含义不清楚

最终值会保存到 ``PMU_REG7B`` 里面。示例代码如下：

.. code-block:: c

    uint32_t reg_value = aon_pmu_ll_get_r0();
    reg_value |= ((reset_type & 0xf) << 0x4);
    aon_pmu_ll_set_r0(reg_value);

    aon_pmu_ll_set_r25(0x424B55AA);
    aon_pmu_ll_set_r25(0xBDB4AA55);

关于 3V 域下 PMU_REG0 的读操作：

.. code-block:: c

    uint32_t reg_7b = aon_pmu_ll_get_r7b();