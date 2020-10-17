---
layout: post 
title: FreeRTOS và Cortex M interrupt
categories: embedded
---
RTOS dùng 1 số interrupt để chạy:  

__SVCall__: Supervisal start schedule, 1 lần lúc bắt đầu chạy  

PendSV: force task switch  

Systick: mỗi tick ngắt kiểm tra hàng đợi để chạy tiếp task này hay switch sang task khác  



Nhưng interrupt này có độ ưu tiên = __configKERNEL_INTERRUPT_PRIORITY__ thấp nhất trong hệ thống   



``` bash
taskENTER_CRITICAL(): disable interrupt có prority thấp hơn giá trị 
**configMAX_SYSCALL_INTERRUPT_PRIORITY.** 
```



Xét trường hợp độ ưu tiên ngắt từ 0-7, 0 thấp nhất  

taskENTER_CRITICAL: task k switch được vì interrupt cho RTOS tick bị disable, interrupt thấp hơn **configMAX_SYSCALL_INTERRUPT_PRIORITY** cũng bị dis(M3/M4/M7)  

M0 thì dis toàn bộ, k quan tâm đến __configMAX_SYSCALL_INTERRUPT_PRIORITY__  

VD:  **configMAX_SYSCALL_INTERRUPT_PRIORITY  = 4,** [taskENTER](https://www.freertos.org/taskENTER_CRITICAL_taskEXIT_CRITICAL.html)[_CRITICAL](https://www.notion.so/FreeRTOS-v-Cortex-M-interrupt-76e5277bfb61442fb7c6c13940d1f016#79d42dedf25d4a4b8760a36d32ca73c0)() sẽ dis interupt ≤4 là 0,1,2,3,4...  

Dùng __vTaskSuspendAll__() đỡ nguy hiểm hơn  



-Trong interrupt k được gọi RTOS function bình thường, chỉ gọi mấy thằng fromISR() như: xTaskNotifyFromISR() ....   

-Interrupt có độ ưu tiên thấp hơn **configMAX_SYSCALL_INTERRUPT_PRIORITY mới dc gọi mất hàm ...FromISR(), cao hơn thì k disable với**  [taskENTER](https://www.freertos.org/taskENTER_CRITICAL_taskEXIT_CRITICAL.html)[_CRITICAL](https://www.notion.so/FreeRTOS-v-Cortex-M-interrupt-76e5277bfb61442fb7c6c13940d1f016#79d42dedf25d4a4b8760a36d32ca73c0)() **dc nên k gọi dc.**  





![/notion2md_output/FreeRTOS va Cortex M interrupt/image/2020-10-16-FreeRTOS-va-Cortex-M-interruptimg_1.png](/notion2md_output/FreeRTOS va Cortex M interrupt/image/2020-10-16-FreeRTOS-va-Cortex-M-interruptimg_1.png)

Lưu ý:   



Priority của task: 0 thấp nhất  

Priority của interrupt trong M3/M4: 8 bits, 255 thấp nhất 0 cao nhất: nên grab hàm set interrupt lại thuận chiều cho đỡ nhầm  



[ARM Cortex-M Interrupts and FreeRTOS: Part 3](https://mcuoneclipse.com/2016/08/28/arm-cortex-m-interrupts-and-freertos-part-3/)

[FreeRTOS - The Free RTOS configuration constants and configuration options - FREE Open Source RTOS for small real time embedded systems](https://www.freertos.org/a00110.html#kernel_priority)