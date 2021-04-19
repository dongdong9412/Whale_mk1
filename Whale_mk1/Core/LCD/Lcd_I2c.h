/*
 * Lcd_I2C.h
 *
 *  Created on: 2021. 4. 5.
 *      Author: exon9
 */

#ifndef LCD_LCD_I2C_H_
#define LCD_LCD_I2C_H_

#include "../Inc/main.h"
#include "stm32f4xx_hal.h"
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>


/* LCD Commands */
#define LCD_CLEARDISPLAY    0x01
#define LCD_RETURNHOME      0x02
#define LCD_ENTRYMODESET    0x04
#define LCD_DISPLAYCONTROL  0x08
#define LCD_CURSORSHIFT     0x10
#define LCD_FUNCTIONSET     0x20
#define LCD_SETCGRAMADDR    0x40
#define LCD_SETDDRAMADDR    0x80

/* Commands bitfields */
//1) Entry mode Bitfields
#define LCD_ENTRY_SH      0x01
#define LCD_ENTRY_ID      0x02
//2) Display control
#define LCD_DISPLAY_B     0x01
#define LCD_DISPLAY_C     0x02
#define LCD_DISPLAY_D     0x04
//3) Shift control
#define LCD_SHIFT_RL      0x04
#define LCD_SHIFT_SC      0x08
//4) Function set control
#define LCD_FUNCTION_F    0x04
#define LCD_FUNCTION_N    0x08
#define LCD_FUNCTION_DL   0x10

/* I2C Control bits */
#define LCD_RS        (1 << 0)
#define LCD_RW        (1 << 1)
#define LCD_EN        (1 << 2)
#define LCD_BK_LIGHT  (1 << 3)

extern bool LCD_i2c_init(I2C_HandleTypeDef *pI2cHandle);

extern void LCD_i2c_setCursor(uint8_t row, uint8_t col);
extern void LCD_i2c_1stLine(void);
extern void LCD_i2c_2ndLine(void);
extern void LCD_i2c_TwoLines(void);
extern void LCD_i2c_OneLine(void);

extern void LCD_i2c_cursorShow(bool state);
extern void LCD_i2c_clear(void);
extern void LCD_i2c_printf(const char* str, ...);


#endif /* LCD_LCD_I2C_H_ */
