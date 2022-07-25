队列
=====

环形缓冲区
----------

环形缓冲区只不过是一个数组。

开始时, r=w=0, 表示没有数据;

写数据时,

.. code-block:: c

    buf[w] = val;
    w = w + 1;
    if (w == 5) {
        w = 0;
    }

读数据时,

.. code-block:: c

    val = buf[r];
    r++;
    if (r == 5) {
        r = 0;
    }

环形缓冲区的优点：
 - 简单
 - 可以解决一个读、一个写的同步问题

环形缓冲区的缺点：
 - 多个读或者多个写, 需要增加互斥操作
 - 没有休眠唤醒机制

队列在环形缓冲区的基础上, 除了增加了互斥操作外, 还增加了休眠-唤醒的操作。

队列数据结构
--------------------

.. code-block:: c
    :linenos:

    typedef struct QueueDefinition 		/* The old naming convention is used to prevent breaking kernel aware debuggers. */
    {
        int8_t *pcHead;					/*< Points to the beginning of the queue storage area. */
        int8_t *pcWriteTo;				/*< Points to the free next place in the storage area. */

        union
        {
            QueuePointers_t xQueue;		/*< Data required exclusively when this structure is used as a queue. */
            SemaphoreData_t xSemaphore; /*< Data required exclusively when this structure is used as a semaphore. */
        } u;

        List_t xTasksWaitingToSend;		/*< List of tasks that are blocked waiting to post onto this queue.  Stored in priority order. */
        List_t xTasksWaitingToReceive;	/*< List of tasks that are blocked waiting to read from this queue.  Stored in priority order. */

        volatile UBaseType_t uxMessagesWaiting;/*< The number of items currently in the queue. */
        UBaseType_t uxLength;			/*< The length of the queue defined as the number of items it will hold, not the number of bytes. */
        UBaseType_t uxItemSize;			/*< The size of each items that the queue will hold. */

        volatile int8_t cRxLock;		/*< Stores the number of items received from the queue (removed from the queue) while the queue was locked.  Set to queueUNLOCKED when the queue is not locked. */
        volatile int8_t cTxLock;		/*< Stores the number of items transmitted to the queue (added to the queue) while the queue was locked.  Set to queueUNLOCKED when the queue is not locked. */

    #if( ( configSUPPORT_STATIC_ALLOCATION == 1 ) && ( configSUPPORT_DYNAMIC_ALLOCATION == 1 ) )
        uint8_t ucStaticallyAllocated;	/*< Set to pdTRUE if the memory used by the queue was statically allocated to ensure no attempt is made to free the memory. */
    #endif

    #if ( configUSE_QUEUE_SETS == 1 )
        struct QueueDefinition *pxQueueSetContainer;
    #endif

    #if ( configUSE_TRACE_FACILITY == 1 )
        UBaseType_t uxQueueNumber;
        uint8_t ucQueueType;
    #endif
    } xQUEUE;

创建队列
--------------------