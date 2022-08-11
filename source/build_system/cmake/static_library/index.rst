====================
构建和链接静态库
====================

link_libraries
===============

.. code-block:: cmake

    link_libraries(libm.a) #contian sin() cos()
    link_libraries(libgcc.a)
    link_libraries(libc.a) #contain memset() memcopy()
    link_libraries(libnosys.a) #contain _write()