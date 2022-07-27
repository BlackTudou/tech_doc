=====
队列
=====

环形缓冲区
==============

环形缓冲区只不过是一个数组。

::

    buf[5]
    -------------------------
    | 0 | 1 | 2 | 3 | 4 | 5 |
    -------------------------
    ^
    |
    r=w=0

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

**环形缓冲区的优点:**
 - 简单
 - 可以解决一个读、一个写的同步问题

**环形缓冲区的缺点：**
 - 多个读或者多个写, 需要增加互斥操作
 - 没有休眠唤醒机制

队列在环形缓冲区的基础上，
 - 增加了互斥操作
 - 增加了休眠-唤醒的操作

队列数据结构
=================

队列涉及：
 - 数据的读写：环形buffer
 - 任务的休眠唤醒：必然有2个链表( ``xTasksWaitingToSend`` 哪些任务在等待空间， ``xTasksWaitingToReceive`` 哪些任务在等待数据)
 - 数据数量的统计

队列的结构体如下：

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

    typedef struct QueuePointers
    {
        int8_t *pcTail;					/*< Points to the byte at the end of the queue storage area.  Once more byte is allocated than necessary to store the queue items, this is used as a marker. */
        int8_t *pcReadFrom;				/*< Points to the last place that a queued item was read from when the structure is used as a queue. */
    } QueuePointers_t;

其中，Line 4、Line 39 对应环形buffer
 - pcWriteTo, pcReadFrom
 - pcHead, pcTail
 - uxLength：队列长度，就是可以容纳多少个元素
 - uxItemSize：队列中一个元素的大小
 - uxMessagesWaiting

创建队列
==============

::

            不同的创建函数                                                                                       对应的参数
    ----------------------------------                都是调用这个函数                -------------------------------------------------------
    | xQueueCreate                   |   ----------------------------------------   | (user_param, user_param, queueQUEUE_TYPE_BASE)       |
    | xQueueCreateSet                |   | QueueHandle_t xQueueGenericCreate(   |   | (user_param, sizeof(Queue_t *), queueQUEUE_TYPE_SET) |
    | xSemaphoreCreateCounting       |   |     const UBaseType_t uxQueueLength, |   | (user_param, 0, queueQUEUE_TYPE_COUNTING_SEMAPHORE)  |
    | xSemaphoreCreateBinary         |-->|     const UBaseType_t uxItemSize,    |-->| (1, 0, queueQUEUE_TYPE_BINARY_SEMAPHORE)             |
    | xSemaphoreCreateMutex          |   |     const uint8_t ucQueueType )      |   | (1, 0, queueQUEUE_TYPE_MUTEX)                        |
    | xSemaphoreCreateRecursiveMutex |   ----------------------------------------   | (1, 0, queueQUEUE_TYPE_RECURSIVE_MUTEX)              |
    ----------------------------------                                              --------------------------------------------------------

理解了队列之后，对其他的信号量、互斥量，也基本理解的差不多了。

 - 队列：涉及数据的读写、数据数目的增减
 - 信号量/互斥量：不涉及数据的读写，只涉及数目的增减

所以，从这个角度看，我们可以使用 ``generic queue`` 来统一队列、信号量、互斥量。

----------------
xQueueCreate
----------------

.. code-block:: c
    :linenos:

    xQueueHandle = xQueueCreate(2, sizeof(int));
    if (xQueueHandle == NULL) {
        printf("create queue failed\r\n");
    }

    #if( configSUPPORT_DYNAMIC_ALLOCATION == 1 )
        #define xQueueCreate( uxQueueLength, uxItemSize ) xQueueGenericCreate( ( uxQueueLength ), ( uxItemSize ), ( queueQUEUE_TYPE_BASE ) )
    #endif
    QueueHandle_t xQueueGenericCreate( const UBaseType_t uxQueueLength, const UBaseType_t uxItemSize, const uint8_t ucQueueType )

可以看到，创建队列时传入两个参数：
 - 环形缓冲区中有多少个元素
 - 每个元素的大小是多少

------------------------
xQueueGenericCreate
------------------------

.. code-block:: c
    :linenos:

    QueueHandle_t xQueueGenericCreate( const UBaseType_t uxQueueLength, const UBaseType_t uxItemSize, const uint8_t ucQueueType )
    {
        Queue_t *pxNewQueue;
        size_t xQueueSizeInBytes;
        uint8_t *pucQueueStorage;

        configASSERT( uxQueueLength > ( UBaseType_t ) 0 );

        if( uxItemSize == ( UBaseType_t ) 0 )
        {
            /* There is not going to be a queue storage area. */
            xQueueSizeInBytes = ( size_t ) 0;
        }
        else
        {
            /* Allocate enough space to hold the maximum number of items that
            can be in the queue at any time. */
            xQueueSizeInBytes = ( size_t ) ( uxQueueLength * uxItemSize ); /*lint !e961 MISRA exception as the casts are only redundant for some ports. */
        }

        /* Allocate the queue and storage area.  Justification for MISRA
        deviation as follows:  pvPortMalloc() always ensures returned memory
        blocks are aligned per the requirements of the MCU stack.  In this case
        pvPortMalloc() must return a pointer that is guaranteed to meet the
        alignment requirements of the Queue_t structure - which in this case
        is an int8_t *.  Therefore, whenever the stack alignment requirements
        are greater than or equal to the pointer to char requirements the cast
        is safe.  In other cases alignment requirements are not strict (one or
        two bytes). */
        pxNewQueue = ( Queue_t * ) pvPortMalloc( sizeof( Queue_t ) + xQueueSizeInBytes ); /*lint !e9087 !e9079 see comment above. */

        if( pxNewQueue != NULL )
        {
            /* Jump past the queue structure to find the location of the queue
            storage area. */
            pucQueueStorage = ( uint8_t * ) pxNewQueue;
            pucQueueStorage += sizeof( Queue_t ); /*lint !e9016 Pointer arithmetic allowed on char types, especially when it assists conveying intent. */

        #if( configSUPPORT_STATIC_ALLOCATION == 1 )
            {
            /* Queues can be created either statically or dynamically, so
            note this task was created dynamically in case it is later
            deleted. */
            pxNewQueue->ucStaticallyAllocated = pdFALSE;
            }
        #endif /* configSUPPORT_STATIC_ALLOCATION */

            prvInitialiseNewQueue( uxQueueLength, uxItemSize, pucQueueStorage, ucQueueType, pxNewQueue );
        }
        else
        {
            traceQUEUE_CREATE_FAILED( ucQueueType );
            mtCOVERAGE_TEST_MARKER();
        }

        return pxNewQueue;
    }

代码分析：
 - Line 30：对于队列，传输数据的大小由用户指定，创建队列时会去创建一个队列结构体，紧随其后还会创建存储数据的环形缓冲区
 - Line 48：分配好内存后，就去初始化队列

------------------------
prvInitialiseNewQueue
------------------------

.. code-block:: c
    :linenos:

    static void prvInitialiseNewQueue( const UBaseType_t uxQueueLength, const UBaseType_t uxItemSize, uint8_t *pucQueueStorage, const uint8_t ucQueueType, Queue_t *pxNewQueue )
    {
        /* Remove compiler warnings about unused parameters should
        configUSE_TRACE_FACILITY not be set to 1. */
        ( void ) ucQueueType;

        if( uxItemSize == ( UBaseType_t ) 0 )
        {
            /* No RAM was allocated for the queue storage area, but PC head cannot
            be set to NULL because NULL is used as a key to say the queue is used as
            a mutex.  Therefore just set pcHead to point to the queue as a benign
            value that is known to be within the memory map. */
            pxNewQueue->pcHead = ( int8_t * ) pxNewQueue;
        }
        else
        {
            /* Set the head to the start of the queue storage area. */
            pxNewQueue->pcHead = ( int8_t * ) pucQueueStorage;
        }

        /* Initialise the queue members as described where the queue type is
        defined. */
        pxNewQueue->uxLength = uxQueueLength;
        pxNewQueue->uxItemSize = uxItemSize;
        ( void ) xQueueGenericReset( pxNewQueue, pdTRUE );

        #if ( configUSE_TRACE_FACILITY == 1 )
        {
            pxNewQueue->ucQueueType = ucQueueType;
        }
        #endif /* configUSE_TRACE_FACILITY */

        #if( configUSE_QUEUE_SETS == 1 )
        {
            pxNewQueue->pxQueueSetContainer = NULL;
        }
        #endif /* configUSE_QUEUE_SETS */

        traceQUEUE_CREATE( pxNewQueue );
    }

    BaseType_t xQueueGenericReset( QueueHandle_t xQueue, BaseType_t xNewQueue )
    {
        Queue_t * const pxQueue = xQueue;

        configASSERT( pxQueue );

        taskENTER_CRITICAL();
        {
            pxQueue->u.xQueue.pcTail = pxQueue->pcHead + ( pxQueue->uxLength * pxQueue->uxItemSize ); /*lint !e9016 Pointer arithmetic allowed on char types, especially when it assists conveying intent. */
            pxQueue->uxMessagesWaiting = ( UBaseType_t ) 0U;
            pxQueue->pcWriteTo = pxQueue->pcHead;
            pxQueue->u.xQueue.pcReadFrom = pxQueue->pcHead + ( ( pxQueue->uxLength - 1U ) * pxQueue->uxItemSize ); /*lint !e9016 Pointer arithmetic allowed on char types, especially when it assists conveying intent. */
            pxQueue->cRxLock = queueUNLOCKED;
            pxQueue->cTxLock = queueUNLOCKED;

            if( xNewQueue == pdFALSE )
            {
                /* If there are tasks blocked waiting to read from the queue, then
                the tasks will remain blocked as after this function exits the queue
                will still be empty.  If there are tasks blocked waiting to write to
                the queue, then one should be unblocked as after this function exits
                it will be possible to write to it. */
                if( listLIST_IS_EMPTY( &( pxQueue->xTasksWaitingToSend ) ) == pdFALSE )
                {
                    if( xTaskRemoveFromEventList( &( pxQueue->xTasksWaitingToSend ) ) != pdFALSE )
                    {
                        queueYIELD_IF_USING_PREEMPTION();
                    }
                    else
                    {
                        mtCOVERAGE_TEST_MARKER();
                    }
                }
                else
                {
                    mtCOVERAGE_TEST_MARKER();
                }
            }
            else
            {
                /* Ensure the event queues start in the correct state. */
                vListInitialise( &( pxQueue->xTasksWaitingToSend ) );
                vListInitialise( &( pxQueue->xTasksWaitingToReceive ) );
            }
        }
        taskEXIT_CRITICAL();

        /* A value is returned for calling semantic consistency with previous
        versions. */
        return pdPASS;
    }

初始化队列，就是去初始化 ``Queue_t`` 这个结构体：
 - Line 18： ``pcHead`` 指向 ``buffer`` 首地址
 - Line 23： ``uxLength`` 队列长度，就是可以容纳多少个元素
 - Line 24： ``uxItemSize`` 队列中一个元素的大小
 - Line 50-55： ``xQueueGenericReset``

   - ``pcTail`` 指向 ``buffer`` 结束位置
   - ``uxMessagesWaiting`` 队列中有多少个有效元素，初始值为0
   - ``pcWriteTo`` 指向 ``buffer`` 首地址
   - ``pcReadFrom`` 指向 ``buffer`` 结束位置

往队列里写数据
===============

**写队列，没有空间导致阻塞，被唤醒** 流程讲解：

--------------
xQueueSend
--------------

.. code-block:: c
    :linenos:

    int sum = 100;
    QueueHandle_t xQueueHandle = xQueueCreate(2, sizeof(int));
    if (xQueueHandle == NULL) {
        printf("create queue failed\r\n");
    }
    xQueueSend(xQueueHandle, &sum, portMAX_DELAY);

    #define xQueueSend( xQueue, pvItemToQueue, xTicksToWait ) xQueueGenericSend( ( xQueue ), ( pvItemToQueue ), ( xTicksToWait ), queueSEND_TO_BACK )

Line 2 创建长度为2的队列，假设一开始没有读任务，它写队列时，第1次成功，第2次成功，第3次休眠。

--------------------
xQueueGenericSend
--------------------

.. code-block:: c
    :linenos:

    BaseType_t xQueueGenericSend( QueueHandle_t xQueue, const void * const pvItemToQueue, TickType_t xTicksToWait, const BaseType_t xCopyPosition )
    {
        BaseType_t xEntryTimeSet = pdFALSE, xYieldRequired;
        TimeOut_t xTimeOut;
        Queue_t * const pxQueue = xQueue;

        /*lint -save -e904 This function relaxes the coding standard somewhat to
        allow return statements within the function itself.  This is done in the
        interest of execution time efficiency. */
        for( ;; )
        {
            /* 关中断 */
            taskENTER_CRITICAL();
            {
                /* Is there room on the queue now?  The running task must be the
                highest priority task wanting to access the queue.  If the head item
                in the queue is to be overwritten then it does not matter if the
                queue is full. */
                /* 有没有空间 */
                if( ( pxQueue->uxMessagesWaiting < pxQueue->uxLength ) || ( xCopyPosition == queueOVERWRITE ) )
                {
                    traceQUEUE_SEND( pxQueue );

                    /* 有空间就写入数据 */
                    xYieldRequired = prvCopyDataToQueue( pxQueue, pvItemToQueue, xCopyPosition );

                    /* If there was a task waiting for data to arrive on the
                    queue then unblock it now. */
                    /* 有没有任务在等待数据 */
                    if( listLIST_IS_EMPTY( &( pxQueue->xTasksWaitingToReceive ) ) == pdFALSE )
                    {
                        /* 有任务在等待数据的话就把它唤醒 */
                        if( xTaskRemoveFromEventList( &( pxQueue->xTasksWaitingToReceive ) ) != pdFALSE )
                        {
                            /* The unblocked task has a priority higher than
                            our own so yield immediately.  Yes it is ok to do
                            this from within the critical section - the kernel
                            takes care of that. */
                            /* 触发一次调度 */
                            queueYIELD_IF_USING_PREEMPTION();
                        }
                        else
                        {
                            mtCOVERAGE_TEST_MARKER();
                        }
                    }
                    else if( xYieldRequired != pdFALSE )
                    {
                        /* This path is a special case that will only get
                        executed if the task was holding multiple mutexes and
                        the mutexes were given back in an order that is
                        different to that in which they were taken. */
                        queueYIELD_IF_USING_PREEMPTION();
                    }
                    else
                    {
                        mtCOVERAGE_TEST_MARKER();
                    }

                    taskEXIT_CRITICAL();
                    return pdPASS;
                }
                /* 队列满了，走这个分支 */
                else
                {
                    /* 不想等待，直接返回errQUEUE_FULL */
                    if( xTicksToWait == ( TickType_t ) 0 )
                    {
                        /* The queue was full and no block time is specified (or
                        the block time has expired) so leave now. */
                        taskEXIT_CRITICAL();

                        /* Return to the original privilege level before exiting
                        the function. */
                        traceQUEUE_SEND_FAILED( pxQueue );
                        return errQUEUE_FULL;
                    }
                    /* 想等待，初始化1个timeout结构体，它记录当前tick */
                    else if( xEntryTimeSet == pdFALSE )
                    {
                        /* The queue was full and a block time was specified so
                        configure the timeout structure. */
                        vTaskInternalSetTimeOutState( &xTimeOut );
                        xEntryTimeSet = pdTRUE;
                    }
                    else
                    {
                        /* Entry time was already set. */
                        mtCOVERAGE_TEST_MARKER();
                    }
                }
            }
            /* 开中断 */
            taskEXIT_CRITICAL();

            /* Interrupts and other tasks can send to and receive from the queue
            now the critical section has been exited. */
            /* 关闭调度器 */
            vTaskSuspendAll();
            prvLockQueue( pxQueue );

            /* Update the timeout state to see if it has expired yet. */
            /* 没超时 */
            if( xTaskCheckForTimeOut( &xTimeOut, &xTicksToWait ) == pdFALSE )
            {
                /* 队列空间满了 */
                if( prvIsQueueFull( pxQueue ) != pdFALSE )
                {
                    traceBLOCKING_ON_QUEUE_SEND( pxQueue );
                    /* 当前任务阻塞：
                    a.放入delayed list
                    b.放入队列的xTasksWaitingToSend链表 */
                    vTaskPlaceOnEventList( &( pxQueue->xTasksWaitingToSend ), xTicksToWait );

                    /* Unlocking the queue means queue events can effect the
                    event list.  It is possible that interrupts occurring now
                    remove this task from the event list again - but as the
                    scheduler is suspended the task will go onto the pending
                    ready last instead of the actual ready list. */
                    prvUnlockQueue( pxQueue );

                    /* Resuming the scheduler will move tasks from the pending
                    ready list into the ready list - so it is feasible that this
                    task is already in a ready list before it yields - in which
                    case the yield will not cause a context switch unless there
                    is also a higher priority task in the pending ready list. */
                    /* 重新开启调度器后，从C语言角度看，在这2个函数之一里面就出不来了
                    直到被唤醒之后，从这里继续执行，再次执行for循环 */
                    if( xTaskResumeAll() == pdFALSE )
                    {
                        portYIELD_WITHIN_API();
                    }
                }
                else
                {
                    /* Try again. */
                    prvUnlockQueue( pxQueue );
                    ( void ) xTaskResumeAll();
                }
            }
            else
            {
                /* The timeout has expired. */
                prvUnlockQueue( pxQueue );
                ( void ) xTaskResumeAll();

                traceQUEUE_SEND_FAILED( pxQueue );
                return errQUEUE_FULL;
            }
        } /*lint -restore */
    }

第1次，第2次写队列
-----------------------

我们的例子中队列长度为2，第1次、第2次都可以写队列成功，对应Line 25 ``prvCopyDataToQueue``，且每次写入成功，都尝试去唤醒 ``pxQueue->xTasksWaitingToReceive`` 中的第1个任务。

问题：
 1.  ``pxQueue->xTasksWaitingToReceive`` 中的任务处于什么状态？ ready？running？blocked？suspended？

   ``pxQueue->xTasksWaitingToReceive`` 中的任务都是在等待这个队列中的数据，自然处于blocked状态，位于delayed list里面。

   这些任务位于两个链表里：1. delayed list 2. pxQueue->xTasksWaitingToReceive

   第1个list，是任务的state list，状态列表

   第2个list，是事件list，比如队列的list、信号的list、互斥量的list

 2.  ``pxQueue->xTasksWaitingToReceive`` 中的任务是怎么排序的？

   - 高优先级的排在前面
   - 同等优先级的，按休眠时间排序，早休眠的排在前面

第3次写队列
-------------------

 - Line 10：注意这个 for 循环，理解代码的关键
 - Line 65：由于队列长度为2，因此第3次写时，走 ``Line 65`` 这个分支
 - Line 67：如果设置队列超时时间为0，则不想等待，直接返回 ``errQUEUE_FULL``
 - Line 79：想等待，初始化1个timeout结构体，它记录当前tick
 - Line 107: 如果队列满了，走这个分支
 - Line 113：当前任务阻塞：放入delayed list，放入队列的xTasksWaitingToSend链表
 - Line 127-130：重新开启调度器，从C语言的角度看，在这2个函数之一里面就出不来了

现在，一个任务写了3次队列，第3次没成功，阻塞了，因为没空间而阻塞，被放在了 ``pxQueue->xTasksWaitingToSend`` 链表里，另一个任务读取数据后，可以释放空间，唤醒写的任务，
被唤醒之后从 Line 130 继续往下执行，再次执行for循环。

问题：假设在 Line 108 与 Line 109 之间 发生了中断，中断里面去读队列，会有什么缺陷？

假设任务刚判断得知：队列满了，下一步就要进入阻塞状态，如果在进入阻塞状态之前，发生了中断，中断里面去读队列，想唤醒任务，但是写的任务还没阻塞。中断执行完后，任务继续运行往下运行，
它要进入阻塞状态。

好像出问题了：
 - 任务进入阻塞状态
 - 但是队列是有空间的（因为中断里有去读队列）

怎么解决这个矛盾？其实，解决方法很巧妙：
 - Line 100，锁定队列，
 - Line 120， ``prvUnlockQueue`` 解锁队列：这里会判断队列中是否有数据，有的话会让已经阻塞的任务进入ready状态。这个函数里会再次判断，有空间的话，唤醒第1个任务。

.. code-block:: c
    :linenos:

    static void prvUnlockQueue( Queue_t * const pxQueue )
    {
        /* THIS FUNCTION MUST BE CALLED WITH THE SCHEDULER SUSPENDED. */

        /* The lock counts contains the number of extra data items placed or
        removed from the queue while the queue was locked.  When a queue is
        locked items can be added or removed, but the event lists cannot be
        updated. */
        taskENTER_CRITICAL();
        {
            int8_t cTxLock = pxQueue->cTxLock;

            /* See if data was added to the queue while it was locked. */
            while( cTxLock > queueLOCKED_UNMODIFIED )
            {
                /* Tasks that are removed from the event list will get added to
                the pending ready list as the scheduler is still suspended. */
                if( listLIST_IS_EMPTY( &( pxQueue->xTasksWaitingToReceive ) ) == pdFALSE )
                {
                    if( xTaskRemoveFromEventList( &( pxQueue->xTasksWaitingToReceive ) ) != pdFALSE )
                    {
                        /* The task waiting has a higher priority so record that
                        a context switch is required. */
                        vTaskMissedYield();
                    }
                    else
                    {
                        mtCOVERAGE_TEST_MARKER();
                    }
                }
                else
                {
                    break;
                }
                --cTxLock;
            }

            pxQueue->cTxLock = queueUNLOCKED;
        }
        taskEXIT_CRITICAL();

        /* Do the same for the Rx lock. */
        taskENTER_CRITICAL();
        {
            int8_t cRxLock = pxQueue->cRxLock;

            while( cRxLock > queueLOCKED_UNMODIFIED )
            {
                if( listLIST_IS_EMPTY( &( pxQueue->xTasksWaitingToSend ) ) == pdFALSE )
                {
                    if( xTaskRemoveFromEventList( &( pxQueue->xTasksWaitingToSend ) ) != pdFALSE )
                    {
                        vTaskMissedYield();
                    }
                    else
                    {
                        mtCOVERAGE_TEST_MARKER();
                    }

                    --cRxLock;
                }
                else
                {
                    break;
                }
            }

            pxQueue->cRxLock = queueUNLOCKED;
        }
        taskEXIT_CRITICAL();
    }

从队列里读数据
===============

**读队列，没有数据导致阻塞，被唤醒** 流程讲解：

.. code-block:: c
    :linenos:

    void recv_task_func(void *param)
    {
        int val;
        while (1) {
            xQueueReceive(xQueueHandle, &val, portMAX_DELAY);
            printf("sum:%d\r\n", val);
        }
    }

    BaseType_t xQueueReceive( QueueHandle_t xQueue, void * const pvBuffer, TickType_t xTicksToWait ) PRIVILEGED_FUNCTION;

---------------
xQueueReceive
---------------

``xQueueReceive`` 会做什么事情：
 - 读数据
 - 唤醒 **等待空间** 而阻塞的任务

.. code-block:: c
    :linenos:

    BaseType_t xQueueReceive( QueueHandle_t xQueue, void * const pvBuffer, TickType_t xTicksToWait )
    {
        BaseType_t xEntryTimeSet = pdFALSE;
        TimeOut_t xTimeOut;
        Queue_t * const pxQueue = xQueue;

        /*lint -save -e904  This function relaxes the coding standard somewhat to
        allow return statements within the function itself.  This is done in the
        interest of execution time efficiency. */
        for( ;; )
        {
            taskENTER_CRITICAL();
            {
                const UBaseType_t uxMessagesWaiting = pxQueue->uxMessagesWaiting;

                /* Is there data in the queue now?  To be running the calling task
                must be the highest priority task wanting to access the queue. */
                if( uxMessagesWaiting > ( UBaseType_t ) 0 )
                {
                    /* Data available, remove one item. */
                    /* 读出数据 */
                    prvCopyDataFromQueue( pxQueue, pvBuffer );
                    traceQUEUE_RECEIVE( pxQueue );
                    pxQueue->uxMessagesWaiting = uxMessagesWaiting - ( UBaseType_t ) 1;

                    /* There is now space in the queue, were any tasks waiting to
                    post to the queue?  If so, unblock the highest priority waiting
                    task. */
                    /* 如果有任务在等待空间 */
                    if( listLIST_IS_EMPTY( &( pxQueue->xTasksWaitingToSend ) ) == pdFALSE )
                    {
                        /* 唤醒它 */
                        if( xTaskRemoveFromEventList( &( pxQueue->xTasksWaitingToSend ) ) != pdFALSE )
                        {
                            queueYIELD_IF_USING_PREEMPTION();
                        }
                        else
                        {
                            mtCOVERAGE_TEST_MARKER();
                        }
                    }
                    else
                    {
                        mtCOVERAGE_TEST_MARKER();
                    }

                    taskEXIT_CRITICAL();
                    return pdPASS;
                }
                else
                {
                    if( xTicksToWait == ( TickType_t ) 0 )
                    {
                        /* The queue was empty and no block time is specified (or
                        the block time has expired) so leave now. */
                        taskEXIT_CRITICAL();
                        traceQUEUE_RECEIVE_FAILED( pxQueue );
                        return errQUEUE_EMPTY;
                    }
                    else if( xEntryTimeSet == pdFALSE )
                    {
                        /* The queue was empty and a block time was specified so
                        configure the timeout structure. */
                        vTaskInternalSetTimeOutState( &xTimeOut );
                        xEntryTimeSet = pdTRUE;
                    }
                    else
                    {
                        /* Entry time was already set. */
                        mtCOVERAGE_TEST_MARKER();
                    }
                }
            }
            taskEXIT_CRITICAL();

            /* Interrupts and other tasks can send to and receive from the queue
            now the critical section has been exited. */

            vTaskSuspendAll();
            prvLockQueue( pxQueue );

            /* Update the timeout state to see if it has expired yet. */
            if( xTaskCheckForTimeOut( &xTimeOut, &xTicksToWait ) == pdFALSE )
            {
                /* The timeout has not expired.  If the queue is still empty place
                the task on the list of tasks waiting to receive from the queue. */
                if( prvIsQueueEmpty( pxQueue ) != pdFALSE )
                {
                    traceBLOCKING_ON_QUEUE_RECEIVE( pxQueue );
                    vTaskPlaceOnEventList( &( pxQueue->xTasksWaitingToReceive ), xTicksToWait );
                    prvUnlockQueue( pxQueue );
                    if( xTaskResumeAll() == pdFALSE )
                    {
                        portYIELD_WITHIN_API();
                    }
                    else
                    {
                        mtCOVERAGE_TEST_MARKER();
                    }
                }
                else
                {
                    /* The queue contains data again.  Loop back to try and read the
                    data. */
                    prvUnlockQueue( pxQueue );
                    ( void ) xTaskResumeAll();
                }
            }
            else
            {
                /* Timed out.  If there is no data in the queue exit, otherwise loop
                back and attempt to read the data. */
                prvUnlockQueue( pxQueue );
                ( void ) xTaskResumeAll();

                if( prvIsQueueEmpty( pxQueue ) != pdFALSE )
                {
                    traceQUEUE_RECEIVE_FAILED( pxQueue );
                    return errQUEUE_EMPTY;
                }
                else
                {
                    mtCOVERAGE_TEST_MARKER();
                }
            }
        } /*lint -restore */
    }