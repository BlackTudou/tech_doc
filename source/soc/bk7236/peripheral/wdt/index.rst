======
wdt
======

bk7236 中有两组Watchdog：
  - aon_watchdog
  - wdt

下面主要介绍wdt。WDT 时钟源为32K时钟，system 0xa[2:3] clkdiv_wdt 可配分频(0:/1 1:/2 2:/4 3:/16)。

wdt 流程
========

wdt 触发，先将rst 信号给到 PMU，触发NMI, 可以在 NMI 进行一些打印处理(打印当前PC值等)，再过7，8个tick后，根据PMU里面的配置进行复位。

 .. note::

  wdt 触发，先将rst 信号给到 PMU，因此在 NMI_Handler 里面关clock/关wdt（设置period=0）都关不掉wdt，该重启还是会重启。

wdt 计数时间配置
==================

假设想配置 wdt 为1000ms， period 该配置为多少？

假设 system 0xa[2:3] (clkdiv_wdt) = 3, 即16分频

 1 / (32000 x 1/16) = 1 / 2000 = 0.5ms,

因此 wdt 计数值 1 对应 0.5ms，那么 1ms 就是 对应计数值 2，1000ms 即对应计数值 2000。因此需配置 period=2000。

触发wdt时，打印call stack
=========================

需求：当watchdog触发时，我们需要知道哪里触发了watchdog(之前程序运行到了哪里)

如果没有这个逻辑：while (!bk_uart_is_tx_over(bk_get_printf_port()));

会发现串口还没打完，就触发重启。

硬件已经将要发送的数据给到uart 的FIFO，然后uart 1位1位的移位出来往外发，串口比较慢，因此加这个逻辑，判断tx fifo为空，
保证都打印出来。

.. code-block:: c
    :linenos:

    void NMI_Handler(void)
    {
    #if CONFIG_CM_BACKTRACE
      uint32_t lr = __get_LR();
      uint32_t sp = __get_MSP();

      BK_LOGW(TAG, "NMI_Handler\r\n");
      bk_set_printf_sync(true);
      cm_backtrace_fault(lr, sp);
    #endif

      /* wait for print over */
      while (!bk_uart_is_tx_over(bk_get_printf_port()));
      /* set reset modules */
      aon_pmu_drv_wdt_rst_dev_enable();

      while(1);
    }

wdt 测试
=========================

测试命令： ``wdt while``

现在 armino 代码会在 SysTick_Handler 里面去进行喂狗的操作，wdt while 里面 关中断 并执行while(1)的操作，便会触发wdt。