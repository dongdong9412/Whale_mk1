/*
 * UartPacket.c
 *
 *  Created on: Mar 24, 2021
 *      Author: exon9
 */

#include "UartPacket.h"

queue tx_queue;
queue rx_queue;
uint8_t UartPacket_AliveCount;

void UartPacket_Init(){
	for(int i = 0;i < BUFFER_SIZE;i++){
		tx_queue.Buffer[0][i] = 0;
		tx_queue.Buffer[1][i] = 0;
		rx_queue.Buffer[0][i] = 0;
		rx_queue.Buffer[1][i] = 0;
	}
	tx_queue.FrontIndex = 0;
	tx_queue.RearIndex = 0;

	rx_queue.FrontIndex = 0;
	rx_queue.RearIndex = 0;

	UartPacket_AliveCount = 0;
}

void UartPacket_Connecting(){
	while(!System_GetConnectInfo()){

		if(UartPacket_QueueEmpty(rx_queue) == FALSE){
			System_SetConnectInfo(UartPacket_RxTask());
		}

		packet_32bit packet_temp;
		packet_temp.B.rw = READ_COMMAND;
		packet_temp.B.id = SRV_ID_VERSION;
		packet_temp.B.checskum = UartPacket_CreateChecksum(packet_temp.B.rw, packet_temp.B.id, packet_temp.B.data);

		UartPacket_QueuePush(&tx_queue, packet_temp.Byte);

		UartPacket_TxTask();
		HAL_Delay(1);

	}
}

void UartPacket_CheckConnection(){
	packet_32bit packet_temp;

	if(UartPacket_AliveCount > CONNECTION_MAX_COUNT){

	}


	packet_temp.B.rw = READ_COMMAND;
	packet_temp.B.id = SRV_ID_VERSION;
	packet_temp.B.data = 0;
	packet_temp.B.checskum = UartPacket_CreateChecksum(packet_temp.B.rw, packet_temp.B.id, packet_temp.B.data);

	UartPacket_QueuePush(&tx_queue, packet_temp.Byte);

	UartPacket_AliveCount++;
}

uint8_t UartPacket_CreateChecksum(uint8_t rw, uint8_t id, uint16_t data){
	uint8_t checksum_buf;
	uint8_t buf[3];

	buf[0] = ((rw << 6) & 0xC0) | (id & 0x3F);
	buf[1] = (data >> 8) & 0xFF;
	buf[2] = (data & 0xFF);

	checksum_buf = buf[0] + buf[1] + buf[2];
	checksum_buf = (~checksum_buf + 1) & 0xFF;

	return checksum_buf;
}

uint8_t UartPacket_CheckChecksum(packet_32bit packet){
	uint8_t buf[4];
	uint8_t checksum_buf;

	buf[0] = (packet.R >> 24) & 0xFF;
	buf[1] = (packet.R >> 16) & 0xFF;
	buf[2] = (packet.R >> 8) & 0xFF;
	buf[3] = packet.R & 0xFF;

	checksum_buf = (buf[0] + buf[1] + buf[2] + buf[3]) & 0xFF;

	if(checksum_buf == 0){
		return 1;
	}
	else{
		return 0;
	}
}

packet_32bit UartPacket_Encode(packet_32bit packet){
	packet.B.checskum = UartPacket_CreateChecksum(packet.B.rw, packet.B.id, packet.B.data);

	return packet;
}

uint8_t UartPacket_RxTask(){
	uint8_t rtn = false;
	packet_32bit packet;

	if(UartPacket_QueueEmpty(rx_queue) == false){
		UartPacket_QueuePop(&rx_queue, packet.Byte);

		if(UartPacket_CheckChecksum(packet)){
			if(packet.B.rw == WRITE_COMMAND){
				switch(packet.B.id){
				case SRV_ID_VERSION:
					// Read Only
					break;
				case SRV_ID_TORQUE:

					break;
				case SRV_ID_STEERING:

					break;
				case SRV_ID_BATTERY:
					// Read Only
					break;
				default:
					// do nothing
					break;
				}
			}
			else if(packet.B.rw == READ_COMMAND){
				packet_32bit temp;
				switch(packet.B.id){
				case SRV_ID_VERSION:
					temp.B.rw = ANSWER_COMMAND;
					temp.B.id = SRV_ID_VERSION;
					temp.B.data = softwareVersion;
					temp.B.checskum = UartPacket_CreateChecksum(temp.B.rw, temp.B.id, temp.B.data);

					if(UartPacket_QueueFull(tx_queue) == FALSE){
						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					else{
						uint8_t tx_buf[4];
						UartPacket_QueuePop(&tx_queue, tx_buf);

						HAL_UART_Transmit(&huart2, tx_buf, 4, 1000);

						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					break;
				case SRV_ID_TORQUE:

					break;
				case SRV_ID_STEERING:

					break;
				case SRV_ID_BATTERY:
					// Read Only
					break;
				case SRV_ID_AX:
					temp.B.rw = ANSWER_COMMAND;
					temp.B.id = SRV_ID_AX;
					temp.B.data = MPU6050_Get_Ax();
					temp.B.checskum = UartPacket_CreateChecksum(temp.B.rw, temp.B.id, temp.B.data);

					if(UartPacket_QueueFull(tx_queue) == FALSE){
						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					else{
						uint8_t tx_buf[4];
						UartPacket_QueuePop(&tx_queue, tx_buf);

						HAL_UART_Transmit(&huart2, tx_buf, 4, 1000);

						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					break;
				case SRV_ID_AY:
					// Read Only
					temp.B.rw = ANSWER_COMMAND;
					temp.B.id = SRV_ID_AY;
					temp.B.data = MPU6050_Get_Ay();
					temp.B.checskum = UartPacket_CreateChecksum(temp.B.rw, temp.B.id, temp.B.data);

					if(UartPacket_QueueFull(tx_queue) == FALSE){
						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					else{
						uint8_t tx_buf[4];
						UartPacket_QueuePop(&tx_queue, tx_buf);

						HAL_UART_Transmit(&huart2, tx_buf, 4, 1000);

						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					break;
				case SRV_ID_AZ:
					// Read Only
					temp.B.rw = ANSWER_COMMAND;
					temp.B.id = SRV_ID_AZ;
					temp.B.data = MPU6050_Get_Az();
					temp.B.checskum = UartPacket_CreateChecksum(temp.B.rw, temp.B.id, temp.B.data);

					if(UartPacket_QueueFull(tx_queue) == FALSE){
						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					else{
						uint8_t tx_buf[4];
						UartPacket_QueuePop(&tx_queue, tx_buf);

						HAL_UART_Transmit(&huart2, tx_buf, 4, 1000);

						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					break;
				default:
					// do nothing
					break;
				}
			}
			else if(packet.B.rw == ANSWER_COMMAND){
				switch(packet.B.id){
				case SRV_ID_VERSION:
					if(packet.B.data == softwareVersion){
						if(UartPacket_AliveCount > 0){
							UartPacket_AliveCount--;
						}
						else{
							// do nothing
						}
						rtn = true;
					}
					else{
						packet_32bit temp;
						temp.B.rw = READ_COMMAND;
						temp.B.id = SRV_ID_VERSION;
						temp.B.data = 0x0;
						temp.B.checskum = UartPacket_CreateChecksum(temp.B.rw, temp.B.id, temp.B.data);

						UartPacket_QueuePush(&tx_queue, temp.Byte);
					}
					break;
				case SRV_ID_TORQUE:

					break;
				case SRV_ID_STEERING:

					break;
				case SRV_ID_BATTERY:
					// Read Only
					break;
				default:
					// do nothing
					break;
				}
			}
			else{
				// do nothing
			}
		}
		else{

		}
	}
	else{
		// Rx queue Empty
	}

	return rtn;
}

void UartPacket_TxTask(){
	uint8_t temp[4];

	if(UartPacket_QueueEmpty(tx_queue) == false){
		uint8_t tx_buf[4];
		UartPacket_QueuePop(&tx_queue, temp);

		tx_buf[3] = temp[0];
		tx_buf[2] = temp[1];
		tx_buf[1] = temp[2];
		tx_buf[0] = temp[3];


		HAL_UART_Transmit(&huart2, tx_buf, 4, 1000);
	}
	else{
		// do nothing
	}
}

uint8_t UartPacket_QueueEmpty(queue Queue){
	if(Queue.FrontIndex == Queue.RearIndex){
		return TRUE;
	}
	else{
		return FALSE;
	}
}

uint8_t UartPacket_QueueFull(queue Queue){
	if(Queue.FrontIndex == ((Queue.RearIndex + 1) % QUEUE_SIZE)){
		return TRUE;
	}
	else{
		return FALSE;
	}
}

void UartPacket_QueuePush(queue *Queue, uint8_t *buf){
	Queue->Buffer[Queue->RearIndex][0] = buf[0];
	Queue->Buffer[Queue->RearIndex][1] = buf[1];
	Queue->Buffer[Queue->RearIndex][2] = buf[2];
	Queue->Buffer[Queue->RearIndex][3] = buf[3];

	Queue->RearIndex = (Queue->RearIndex + 1) % QUEUE_SIZE;
}

void UartPacket_QueuePop(queue *Queue, uint8_t *buf){
	buf[0] = Queue->Buffer[Queue->FrontIndex][0];
	buf[1] = Queue->Buffer[Queue->FrontIndex][1];
	buf[2] = Queue->Buffer[Queue->FrontIndex][2];
	buf[3] = Queue->Buffer[Queue->FrontIndex][3];
	Queue->FrontIndex = (Queue->FrontIndex + 1) % QUEUE_SIZE;
}
