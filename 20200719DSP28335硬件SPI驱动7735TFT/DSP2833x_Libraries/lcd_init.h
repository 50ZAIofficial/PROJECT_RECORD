#ifndef __LCD_INIT_H
#define __LCD_INIT_H


#define USE_HORIZONTAL 1  //设置横屏或者竖屏显示 0或1为竖屏 2或3为横屏


#if USE_HORIZONTAL==0||USE_HORIZONTAL==1
#define LCD_W 128
#define LCD_H 160

#else
#define LCD_W 160
#define LCD_H 128
#endif


#include "DSP2833x_Device.h"     // DSP2833x Headerfile Include File
#include "DSP2833x_Examples.h"   // DSP2833x Examples Include File
#include "leds.h"

#define u8  unsigned char
#define u16 unsigned int
#define u32 unsigned long int

//-----------------LCD端口定义----------------

void SpiIsr();
void SpiInt();
void delay_ms(unsigned int ms);//不准确延时函数
void LCD_GPIO_Init(void);//初始化GPIO
void LCD_Writ_Bus(u8 dat);//模拟SPI时序
void LCD_WR_DATA8(u8 dat);//写入一个字节
void LCD_WR_DATA(u16 dat);//写入两个字节
void LCD_WR_REG(u8 dat);//写入一个指令
void LCD_Address_Set(u16 x1,u16 y1,u16 x2,u16 y2);//设置坐标函数
void Lcd_Init(void);//LCD初始化

unsigned char SPIx_ReadWriteByte(unsigned char TxData);

#define LCD_RES_Clr() LED5_ON//RES64
#define LCD_RES_Set() LED5_OFF

#define LCD_DC_Clr() LED4_ON//DC65
#define LCD_DC_Set() LED4_OFF

//#define LCD_CS_Clr()  LED2_ON//CS67
//#define LCD_CS_Set()  LED2_OFF

#define LCD_BLK_Clr()  LED3_ON//BLK66
#define LCD_BLK_Set()  LED3_OFF




#endif

