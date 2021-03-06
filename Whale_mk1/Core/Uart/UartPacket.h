/*
 * UartPacket.h
 *
 *  Created on: Mar 24, 2021
 *      Author: exon9
 */

#ifndef UART_UARTPACKET_H_
#define UART_UARTPACKET_H_

#include "../Inc/main.h"
#include "../Inc/Project.h"
#include "../System/System.h"
#include <stdbool.h>


#define READ_COMMAND 			0
#define WRITE_COMMAND 			1
#define ANSWER_COMMAND 			2

#define SRV_ID_VERSION			0
#define SRV_ID_TORQUE			1
#define SRV_ID_STEERING			2
#define SRV_ID_BATTERY			3
#define SRV_ID_AX				4
#define SRV_ID_AY				5
#define SRV_ID_AZ				6


#define BUFFER_SIZE				4
#define QUEUE_SIZE				10

#define CONNECTION_MAX_COUNT	100


typedef union packet_32bit_tag{
	uint32_t R;
	uint8_t Byte[4];
	struct{
		uint32_t checskum:8;
		uint32_t data:16;
		uint32_t id:6;
		uint32_t rw:2;
	}B;
}packet_32bit;

typedef struct queue_tag{
	uint8_t Buffer[QUEUE_SIZE][BUFFER_SIZE];
	uint8_t FrontIndex;
	uint8_t RearIndex;
}queue;


extern queue tx_queue;
extern queue rx_queue;


extern void UartPacket_Init();
extern void UartPacket_Connecting();
extern void UartPacket_CheckConnection();
extern uint8_t UartPacket_CreateChecksum(uint8_t rw, uint8_t id, uint16_t data);
extern uint8_t UartPacket_CheckChecksum(packet_32bit packet);
extern packet_32bit UartPacket_Encode(packet_32bit packet);
extern uint8_t UartPacket_RxTask();
extern void UartPacket_TxTask();
extern uint8_t UartPacket_QueueEmpty(queue Queue);
extern uint8_t UartPacket_QueueFull(queue Queue);
extern void UartPacket_QueuePush(queue *Queue, uint8_t *buf);
extern void UartPacket_QueuePop(queue *Queue, uint8_t *buf);

#endif /* UART_UARTPACKET_H_ */
