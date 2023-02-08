=========
Linux
=========

tar -jcvf test.gz.bz2 abd.txt bcd.txt
tar -jxvf test.gz.bz2

.tar.gz 格式解压 tar -zxvf xx.tar.gz

.tar.bz2 格式解压 tar -jxvf xx.tar.bz2

sed
====

在 h264.txt 文件每行行首添加 0x

.. code-block:: shell

    sed "s/^/&0x/g" h264.txt