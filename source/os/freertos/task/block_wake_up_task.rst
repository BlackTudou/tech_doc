==============
任务阻塞/唤醒
==============

vTaskDelay
===========

.. code-block:: c
    :linenos:

    void vTaskDelay( const TickType_t xTicksToDelay )
    {
        BaseType_t xAlreadyYielded = pdFALSE;

        /* A delay time of zero just forces a reschedule. */
        if( xTicksToDelay > ( TickType_t ) 0U )
        {
            configASSERT( uxSchedulerSuspended == 0 );
            vTaskSuspendAll();
            {
                traceTASK_DELAY();

                /* A task that is removed from the event list while the
                scheduler is suspended will not get placed in the ready
                list or removed from the blocked list until the scheduler
                is resumed.

                This task cannot be in an event list as it is the currently
                executing task. */
                /* 把自己从ready list移除，放入delayed list */
                prvAddCurrentTaskToDelayedList( xTicksToDelay, pdFALSE );
            }
            /* 要么在这函数发起调度 */
            xAlreadyYielded = xTaskResumeAll();
        }
        else
        {
            mtCOVERAGE_TEST_MARKER();
        }

        /* Force a reschedule if xTaskResumeAll has not already done so, we may
        have put ourselves to sleep. */
        if( xAlreadyYielded == pdFALSE )
        {
            /* 要么在这函数发起调度 */
            portYIELD_WITHIN_API();
        }
        else
        {
            mtCOVERAGE_TEST_MARKER();
        }
    }

难点在于：有两个delayed list
 - pxDelayedTaskList：指向当前的delayed list
 - pxOverflowDelayedTaskList：指向溢出的delayed list

.. code-block:: c
    :linenos:

    PRIVILEGED_DATA static List_t * volatile pxDelayedTaskList;            /*< Points to the delayed task list currently being used. */
    PRIVILEGED_DATA static List_t * volatile pxOverflowDelayedTaskList;    /*< Points to the delayed task list currently being used to hold tasks that have overflowed the current tick count. */

    static void prvInitialiseTaskLists( void )
    {
        UBaseType_t uxPriority;

        for( uxPriority = ( UBaseType_t ) 0U; uxPriority < ( UBaseType_t ) configMAX_PRIORITIES; uxPriority++ )
        {
            vListInitialise( &( pxReadyTasksLists[ uxPriority ] ) );
        }

        vListInitialise( &xDelayedTaskList1 );
        vListInitialise( &xDelayedTaskList2 );
        vListInitialise( &xPendingReadyList );

        #if ( INCLUDE_vTaskDelete == 1 )
        {
            vListInitialise( &xTasksWaitingTermination );
        }
        #endif /* INCLUDE_vTaskDelete */

        #if ( INCLUDE_vTaskSuspend == 1 )
        {
            vListInitialise( &xSuspendedTaskList );
        }
        #endif /* INCLUDE_vTaskSuspend */

        /* Start with pxDelayedTaskList using list1 and the pxOverflowDelayedTaskList
        using list2. */
        pxDelayedTaskList = &xDelayedTaskList1;
        pxOverflowDelayedTaskList = &xDelayedTaskList2;
    }