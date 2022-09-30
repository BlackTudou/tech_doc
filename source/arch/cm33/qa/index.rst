=======
Q&A
=======

问题集锦
=========

1. 中断屏蔽如何解决嵌套问题？
   先看下面的代码：

.. code-block:: c
    :linenos:

    void func(void)
    {
        uint32_t int_level = rtos_disable_int();

        rtos_enable_int(int_level);
    }

    bk_err_t bk_i2c_memory_write()
    {
        uint32_t int_level = rtos_disable_int();

        s_i2c[id].work_mode = I2C_MASTER_WRITE;
        func();
        s_i2c[id].dev_addr = mem_param->dev_addr;

        rtos_enable_int(int_level);
    }

    uint32_t rtos_disable_int(void)
    {
        __disable_irq();
        return 0;
    }

    void rtos_enable_int(uint32_t val)
    {
        __enable_irq();
    }

如上代码， ``Line 12`` - ``Line 14`` 想作为一个原子操作，不被中断打断执行， ``Line 10`` 通过设置 ``PRIMASK`` 屏蔽中断，执行完相关操作后，
``Line 16`` 打开中断。但是在 ``func()`` 也调用了屏蔽打开中断的操作，这会导致在执行完 ``Line 13`` 后，此时中断已经被打开了， 若此时发生中断，
则 ``Line 14`` 会被打断执行，这就是问题所在，我们需要解决这种case下的情况。

.. note::
    PRIMASK 默认值是0，也就是屏蔽（禁止异常/中断）不起作用。在置位时，它会阻止不可屏蔽中断（NMI）和HardFault异常之外的所有异常（包括中断）。

代码修改如下：

.. code-block:: c
    :linenos:

    uint32_t rtos_disable_int(void)
    {
        uint32_t primask_val = __get_PRIMASK();
        __disable_irq();
        return primask_val;
    }

    void rtos_enable_int(uint32_t val)
    {
        __set_PRIMASK(val);
    }

再分析一遍代码执行流程（第一个代码段）：

 - Line 10 屏蔽中断，设置 PRIMASK = 1，返回先前 PRIMASK 的值=0 (PRIMASK 默认值是0)
 - 调用 func(), Line 3 屏蔽中断，返回 PRIMASK的值 = 1
 - Line 5，取消屏蔽中断，设置 PRIMASK = 1， **此时仍然处于屏蔽中断的状态**
 - func()函数执行完成，Line 16，取消屏蔽中断，设置 PRIMASK=0