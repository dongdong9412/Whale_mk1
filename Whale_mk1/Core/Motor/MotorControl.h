/*
 * MotorControl.h
 *
 *  Created on: 2021. 4. 14.
 *      Author: exon9
 */

#ifndef MOTOR_MOTORCONTROL_H_
#define MOTOR_MOTORCONTROL_H_

#include "../Inc/main.h"

typedef struct PID_Control_tag{
	float kP;
	float kI;
	float kD;

	float P_Control;
	float I_Control;
	float D_Control;

	float error;
	float prev_error;
	float I_error;
	float D_error;

	float current;
	float goal;

	float value;
}PID_Control;

extern PID_Control Motor;
extern PID_Control Servo;

extern void MotorControl_Init();
extern void Motor_Forward();
extern void Motor_Backward();

#endif /* MOTOR_MOTORCONTROL_H_ */
