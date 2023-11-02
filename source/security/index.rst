============
security
============

mbedtls
===============

1. sha1.h

mbedtls/include/mbedtls/sha1.h

#define MBEDTLS_SHA1_ALT

2. sha1_alt.h

#define mbedtls_sha1_starts dubhe_sha1_starts

3. sha1.c

accelerator/dubhe_alt/src/sha1.c


mbedtls_sha256_starts
===========================

mbedtls_sha256_starts 调用流程，从 selftest 入手

.. code-block:: text

    mbedtls_sha256_starts
      #define mbedtls_sha256_starts dubhe_sha256_starts
        dubhe_sha256_starts_ret( ctx, is224 );
          arm_ce_hash_start( ctx, ARM_HASH_VECT_DEFAULT, ARM_HASH_IV_IS_ADDR, NULL, 0, hash_mode );
            arm_ce_hash_execute_hash_init( ctx,
                                           ARM_HASH_VECT_DEFAULT,
                                           vect_is_addr,
                                           external_vector,
                                           iv_len,
                                           hash_mode );
              ret = arm_ce_hash_wait_engine_idle( );
                value = arm_ce_hash_read_hash_stat( );

.. note::

    在使用shanhai 加密引擎之前，需要先调用 ``dubhe_driver_init(unsigned long dbh_base_addr)``

.. note::

    注意需要给shanhai 上电，system REG_0x10 BIT[3] pwd_encp，写0上电