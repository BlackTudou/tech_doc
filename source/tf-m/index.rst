======
TF-M
======

armino 运行TF-M
==================

配置文件修改如下：

1. middleware/soc/bk7236/bk7236.defconfig.armino_ns 改为 bk7236.defconfig
2. projects/verify/spe/config/bk7236.config.tfm_s-2-armino_ns 改为 bk7236.config
   projects/verify/spe/config/partitions/partitions.armino_ns 改为 partitions
3. properties/soc/bk7236/bk7236.defconfig.armino_ns 改为 bk7236.defconfig


make bk7236 2&>1


TF-M 启动代码
===============

startup_cmsdk_bk7236_s.S
system_cmsdk_bk7236.c


load_info_ns_agent_tz.c    tfm_sp_ns_agent_tz_load->entry


tfm/secure_fw/spm/cmsis_psa/main.c

tfm_hal_platform.c -> tfm_s_2_ns_hook

-----------
跳转到NS
-----------

**ns_agent_tz.c**

1. 配置NS世界的VTOR， NS的向量表

    SCB_NS->VTOR = tfm_hal_get_ns_VTOR(); 0x12060000

2. 初始化NS世界的主堆栈指针

    __TZ_set_MSP_NS(tfm_hal_get_ns_MSP());

    MSR MSP_NS, R3

3. 初始化NS世界的第一条指令所在地址

    tfm_hal_get_ns_entry_point(); //0x1208 7F24

4. 执行跳转

    BXNS           R0




attest_asymmetric_s_interface_testsuite();


