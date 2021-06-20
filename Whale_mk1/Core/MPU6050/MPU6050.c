/*
 * MPU6050.c
 *
 *  Created on: 2021. 5. 6.
 *      Author: exon9
 */

#include "MPU6050.h"


Gyro_Data GForce;

bool MPU6050_Checksum(uint8_t *data){
	uint8_t checksum = 0;
	for(int i = 0;i < 10;i++){
		checksum += data[i];
	}
	if(checksum == data[10]){
		return true;
	}
	else{
		return false;
	}
}

void MPU6050_Update_Acceleration(uint8_t *data){
	GForce.Ax = ((data[1] << 8) | data[0]);
	GForce.Ay = ((data[3] << 8) | data[2]);
	GForce.Az = ((data[5] << 8) | data[4]);

	GForce.T = ((data[7] << 8) | data[6]);
}

void MPU6050_Update_AngularVelocity(uint8_t *data){
	GForce.Wx = ((data[1] << 8) | data[0]);
	GForce.Wy = ((data[3] << 8) | data[2]);
	GForce.Wz = ((data[5] << 8) | data[4]);

	GForce.T = ((data[7] << 8) | data[6]);
}

void MPU6050_Update_Angle(uint8_t *data){
	GForce.Roll = (float)((data[1] << 8) | data[0]);
	GForce.Pitch = (float)((data[3] << 8) | data[2]);
	GForce.Yaw = (float)((data[5] << 8) | data[4]);

	GForce.T = (float)((data[7] << 8) | data[6]);
}

uint16_t MPU6050_Get_Ax(){
	return GForce.Ax;
}

uint16_t MPU6050_Get_Ay(){
	return GForce.Ay;
}

uint16_t MPU6050_Get_Az(){
	return GForce.Az;
}
