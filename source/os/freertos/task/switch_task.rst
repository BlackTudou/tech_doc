==========
任务切换
==========

vTaskSwitchContext
===================

确定下一个要执行的任务，就是让 ``pxCurrentTCB`` 指向新的任务。

.. code-block:: c
    :linenos:

    void vTaskSwitchContext( void )
    {
        if( uxSchedulerSuspended != ( UBaseType_t ) pdFALSE )
        {
            /* The scheduler is currently suspended - do not allow a context
            switch. */
            xYieldPending = pdTRUE;
        }
        else
        {
            xYieldPending = pdFALSE;
            traceTASK_SWITCHED_OUT();

            /* Check for stack overflow, if configured. */
            taskCHECK_FOR_STACK_OVERFLOW();

            /* Select a new task to run using either the generic C or port
            optimised asm code. */
            taskSELECT_HIGHEST_PRIORITY_TASK(); /*lint !e9079 void * is used as this macro is used with timers and co-routines too.  Alignment is known to be fine as the type of the pointer stored and retrieved is the same. */
            traceTASK_SWITCHED_IN();
        }
    }

``taskSELECT_HIGHEST_PRIORITY_TASK`` 选择高优先级的任务。

查找下一个要运行的任务有两种方法，通过 ``configUSE_PORT_OPTIMISED_TASK_SELECTION`` 来配置。

 - configUSE_PORT_OPTIMISED_TASK_SELECTION = 0， 使用通用方法
 - configUSE_PORT_OPTIMISED_TASK_SELECTION = 1， 使用硬件方法

--------------
通用方法
--------------

.. code-block:: c
    :linenos:

    #define taskSELECT_HIGHEST_PRIORITY_TASK()                                                  \
    {                                                                                           \
        UBaseType_t uxTopPriority = uxTopReadyPriority;                                         \
                                                                                                \
        /* Find the highest priority queue that contains ready tasks. */                        \
        while( listLIST_IS_EMPTY( &( pxReadyTasksLists[ uxTopPriority ] ) ) )                   \
        {                                                                                       \
            configASSERT( uxTopPriority );                                                      \
            --uxTopPriority;                                                                    \
        }                                                                                       \
                                                                                                \
        /* listGET_OWNER_OF_NEXT_ENTRY indexes through the list, so the tasks of                \
        the same priority get an equal share of the processor time. */                          \
        listGET_OWNER_OF_NEXT_ENTRY( pxCurrentTCB, &( pxReadyTasksLists[ uxTopPriority ] ) );   \
        uxTopReadyPriority = uxTopPriority;                                                     \
    } /* taskSELECT_HIGHEST_PRIORITY_TASK */

    #define listGET_OWNER_OF_NEXT_ENTRY( pxTCB, pxList )										\
    {																							\
        List_t * const pxConstList = ( pxList );												\
        /* Increment the index to the next item and return the item, ensuring */				\
        /* we don't return the marker used at the end of the list.  */							\
        ( pxConstList )->pxIndex = ( pxConstList )->pxIndex->pxNext;							\
        if( ( void * ) ( pxConstList )->pxIndex == ( void * ) &( ( pxConstList )->xListEnd ) )	\
        {																						\
            ( pxConstList )->pxIndex = ( pxConstList )->pxIndex->pxNext;						\
        }																						\
        ( pxTCB ) = ( pxConstList )->pxIndex->pvOwner;											\
    }

代码分析：
 - Line 6-10： ``uxTopPriority`` 是一个整数，比如：优先级为5的 ``readylist`` 为空，则继续往下找优先级为4的 ``readylist``，因此，当循环退出后， ``uxTopPriority`` 就是最高优先级

  .. note:: 如果高优先级任务的readylist不为空，则低优先级任务永远没机会执行

 - Line 14：在链表中找出下一个TCB，怎么在一个readylist[xxxx]里确定下一个TCB？ 挪动一下链表的 ``pxIndex`` 就可以了

------------
硬件方法
------------

``CLZ`` 前导零计数(Count Leading Zero)

.. code-block:: c
    :linenos:

    #define taskSELECT_HIGHEST_PRIORITY_TASK()														\
    {																								\
        UBaseType_t uxTopPriority;																	\
                                                                                                    \
        /* Find the highest priority list that contains ready tasks. */								\
        portGET_HIGHEST_PRIORITY( uxTopPriority, uxTopReadyPriority );								\
        configASSERT( listCURRENT_LIST_LENGTH( &( pxReadyTasksLists[ uxTopPriority ] ) ) > 0 );		\
        listGET_OWNER_OF_NEXT_ENTRY( pxCurrentTCB, &( pxReadyTasksLists[ uxTopPriority ] ) );		\
    } /* taskSELECT_HIGHEST_PRIORITY_TASK() */

    #define portGET_HIGHEST_PRIORITY( uxTopPriority, uxReadyPriorities ) uxTopPriority = ( 31UL - ( uint32_t ) __clz( ( uxReadyPriorities ) ) )

``uxTopPriority`` 是一个整数，比如：优先级为5的readylist不空，那么uxTopPriority的bit5就是1，优先级为4的readylist不空，那么uxTopPriority的bit4就是1

__clz 是一个函数，它的本质是一条汇编指令： ``clz`` 前导零计数(Count Leading Zero)。

比如：uxTopPriority 的bit5，bit4，bit0都是1，clz(uxTopPriority)=？就是计算32位的数据里，前面有几个0？bit31~bit6等于0，前面有 31-6+1=26个0。

借助 ``clz`` 命令，很快就可以算出：readylist 不为空的最高优先级为5，uxTopPriority = 31UL - __clz(uxReadyPriorities) = 31 - 26 = 5。所以：FreeRTOS的最高优先级是31，这是为了考虑效率。