/*
 * MotorControl.c
 *
 *  Created on: 2021. 4. 14.
 *      Author: exon9
 */


#include "MotorControl.h"



PID_Control Motor;
PID_Control Servo;


void MotorControl_Init(){
	/* Motor PID */
	Motor.kP = 0;
	Motor.kI = 0;
	Motor.kD = 0;

	Motor.P_Control = 0;
	Motor.I_Control = 0;
	Motor.D_Control = 0;

	Motor.error = 0;
	Motor.prev_error = 0;
	Motor.I_error = 0;
	Motor.D_error = 0;

	Motor.current = 0;
	Motor.goal = 0;

	Motor.value = 0;

	/* Steering PID */
	Servo.kP = 0;
	Servo.kI = 0;
	Servo.kD = 0;

	Servo.P_Control = 0;
	Servo.I_Control = 0;
	Servo.D_Control = 0;

	Servo.error = 0;
	Servo.prev_error = 0;
	Servo.I_error = 0;
	Servo.D_error = 0;

	Servo.current = 0;
	Servo.goal = 0;

	Servo.value = 0;
}
