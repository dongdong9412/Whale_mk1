/*
 * System.h
 *
 *  Created on: 2021. 4. 10.
 *      Author: exon9
 */

#ifndef SYSTEM_SYSTEM_H_
#define SYSTEM_SYSTEM_H_

#include "../Inc/main.h"

#define SYSTEM_10MS_TICK	(10U)
#define SYSTEM_100MS_TICK	(100U)
#define SYSTEM_1S_TICK		(1000U)

#define TASK_NUM			(6U)

typedef struct task_tag{
	uint16_t tick_max;
	uint16_t tick;
	uint8_t activate;
	void (*Function)();
}task;

typedef enum taskName_tag{
	SYSTEM_1MS = 0,
	SYSTEM_10MS_1MS,
	SYSTEM_10MS_6MS,
	SYSTEM_100MS_2MS,
	SYSTEM_100MS_52MS,
	SYSTEM_1S_3MS
}taskName;

typedef enum transmission_tag{
	P = 0,
	R,
	N,
	D
}transmission;

typedef struct system_Info_tag{
	uint8_t uart_connect;
	transmission Transmission;
}system_Info;

extern system_Info whale_Info;

extern void System_Init();
extern void System_Main();
extern void System_TimerManager();
extern void System_Scheduler();
extern uint8_t System_GetConnectInfo();
extern void System_SetConnectInfo(uint8_t flag);

extern void System_1ms_Task();
extern void System_10ms_Task_1ms_Offset();
extern void System_10ms_Task_6ms_Offset();
extern void System_100ms_Task_2ms_Offset();
extern void System_100ms_Task_52ms_Offset();
extern void System_1s_Task_3ms_Offset();

#endif /* SYSTEM_SYSTEM_H_ */
