#ifndef __LCD_INIT_H
#define __LCD_INIT_H


#include "REG52.h"
#include "intrins.h"

#define USE_HORIZONTAL 1  //设置横屏或者竖屏显示 0或1为竖屏 2或3为横屏


#if USE_HORIZONTAL==0||USE_HORIZONTAL==1
#define LCD_W 128
#define LCD_H 160

#else
#define LCD_W 160
#define LCD_H 128
#endif

#define u8  unsigned char
#define u16 unsigned int

//SS_2/P2.2, MOSI_2/P2.3, MISO_2/P2.4, SCLK_2/P2.5

sbit LCD_SCL=P2^5;//SCLK
sbit LCD_SDA=P2^3;//MOSI
sbit LCD_RES=P2^6;//RES
sbit LCD_DC =P2^4;//DC
sbit LCD_CS =P2^2; //CS
sbit LCD_BLK=P2^0; //BLK




//SS/P1.2, MOSI/P1.3, MISO/P1.4, SCLK/P1.5

//-----------------LCD端口定义----------------

#define LCD_SCLK_Clr() LCD_SCL=0//SCL=SCLK
#define LCD_SCLK_Set() LCD_SCL=1

#define LCD_MOSI_Clr() LCD_SDA=0//SDA=MOSI
#define LCD_MOSI_Set() LCD_SDA=1

#define LCD_RES_Clr() LCD_RES=0//RES
#define LCD_RES_Set() LCD_RES=1

#define LCD_DC_Clr() LCD_DC=0//DC
#define LCD_DC_Set() LCD_DC=1

#define LCD_CS_Clr()  LCD_CS=0//CS
#define LCD_CS_Set()  LCD_CS=1

#define LCD_BLK_Clr()  LCD_BLK=0//BLK
#define LCD_BLK_Set()  LCD_BLK=1


sfr     SPSTAT      =   0xcd;
sfr     SPCTL       =   0xce;
sfr     SPDAT       =   0xcf;
sfr     IE2         =   0xaf;
#define ESPI            0x02;
sfr  P5 = 0xC8;//P5地址
sbit     LED=P5^5;

void SpiIsr();
void SpiInt();
void delay_ms(unsigned int ms);//不准确延时函数
void LCD_GPIO_Init(void);//初始化GPIO
void LCD_Writ_Bus(u8 dat);//模拟SPI时序
void LCD_WR_DATA8(u8 dat);//写入一个字节
void LCD_WR_DATA(u16 dat);//写入两个字节
void LCD_WR_REG(u8 dat);//写入一个指令
void LCD_Address_Set(u16 x1,u16 y1,u16 x2,u16 y2);//设置坐标函数
void LCD_Init(void);//LCD初始化
#endif

