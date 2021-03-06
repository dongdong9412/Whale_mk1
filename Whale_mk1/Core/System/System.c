/*
 * System.c
 *
 *  Created on: 2021. 4. 10.
 *      Author: exon9
 */


#include "System.h"

system_Info whale_Info;

task System_Task[TASK_NUM];

void System_Init(){
	whale_Info.uart_connect = FALSE;
	whale_Info.Transmission = P;

	System_Task[SYSTEM_1MS].tick_max = 1;
	System_Task[SYSTEM_1MS].tick = 0;
	System_Task[SYSTEM_1MS].activate = 0;
	System_Task[SYSTEM_1MS].Function = System_1ms_Task;

	System_Task[SYSTEM_10MS_1MS].tick_max = 10;
	System_Task[SYSTEM_10MS_1MS].tick = 9;
	System_Task[SYSTEM_10MS_1MS].activate = 0;
	System_Task[SYSTEM_10MS_1MS].Function = System_10ms_Task_1ms_Offset;

	System_Task[SYSTEM_10MS_6MS].tick_max = 10;
	System_Task[SYSTEM_10MS_6MS].tick = 4;
	System_Task[SYSTEM_10MS_6MS].activate = 0;
	System_Task[SYSTEM_10MS_6MS].Function = System_10ms_Task_6ms_Offset;

	System_Task[SYSTEM_100MS_2MS].tick_max = 100;
	System_Task[SYSTEM_100MS_2MS].tick = 98;
	System_Task[SYSTEM_100MS_2MS].activate = 0;
	System_Task[SYSTEM_100MS_2MS].Function = System_100ms_Task_2ms_Offset;

	System_Task[SYSTEM_100MS_52MS].tick_max = 100;
	System_Task[SYSTEM_100MS_52MS].tick = 52;
	System_Task[SYSTEM_100MS_52MS].activate = 0;
	System_Task[SYSTEM_100MS_52MS].Function = System_100ms_Task_52ms_Offset;

	System_Task[SYSTEM_1S_3MS].tick_max = 1000;
	System_Task[SYSTEM_1S_3MS].tick = 997;
	System_Task[SYSTEM_1S_3MS].activate = 0;
	System_Task[SYSTEM_1S_3MS].Function = System_1s_Task_3ms_Offset;

}

void System_Main(){
	switch(whale_Info.Transmission){
	case P:

		break;
	case R:

		break;
	case N:

		break;
	case D:

		break;
	default:

		break;
	}
}

void System_TimerManager(){
	for(int i = 0;i < TASK_NUM;i++){
		System_Task[i].tick++;
		if(System_Task[i].tick == System_Task[i].tick_max){
			System_Task[i].tick = 0;
			System_Task[i].activate = 1;
		}
	}
}

void System_Scheduler(){
	for(int i = 0;i < TASK_NUM;i++){
		if(System_Task[i].activate == 1){
			System_Task[i].activate = 0;
			System_Task[i].Function();
			break;
		}
	}
}

uint8_t System_GetConnectInfo(){
	return whale_Info.uart_connect;
}

void System_SetConnectInfo(uint8_t flag){
	whale_Info.uart_connect = flag;
}

void System_1ms_Task(){

}

void System_10ms_Task_1ms_Offset(){

}

void System_10ms_Task_6ms_Offset(){

}

void System_100ms_Task_2ms_Offset(){
	UartPacket_CheckConnection();
}

void System_100ms_Task_52ms_Offset(){

}

void System_1s_Task_3ms_Offset(){
	HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
}
