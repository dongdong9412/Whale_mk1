/*
 * MPU6050.h
 *
 *  Created on: 2021. 5. 6.
 *      Author: exon9
 */

#ifndef MPU6050_MPU6050_H_
#define MPU6050_MPU6050_H_

#include "../Inc/main.h"

typedef struct Gyro_Data_tag{
	uint16_t Ax;
	uint16_t Ay;
	uint16_t Az;

	uint16_t Wx;
	uint16_t Wy;
	uint16_t Wz;

	uint16_t Roll;
	uint16_t Pitch;
	uint16_t Yaw;

	uint16_t T;
}Gyro_Data;

extern bool MPU6050_Checksum(uint8_t *data);
extern void MPU6050_Update_Acceleration(uint8_t *data);
extern void MPU6050_Update_AngularVelocity(uint8_t *data);
extern void MPU6050_Update_Angle(uint8_t *data);
extern uint16_t MPU6050_Get_Ax();
extern uint16_t MPU6050_Get_Ay();
extern uint16_t MPU6050_Get_Az();

#endif /* MPU6050_MPU6050_H_ */
