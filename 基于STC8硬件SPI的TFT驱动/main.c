//////////////////////////////////////////////////////////////////////////////////	 
//本程序只供学习使用，未经作者许可，不得用于其它任何用途
//中景园电子
//店铺地址：http://shop73023976.taobao.com/?spm=2013.1.0.0.M4PqC2
//
//  文 件 名   : main.c
//  版 本 号   : v2.0
//  作    者   : HuangKai
//  生成日期   : 2014-0101
//  最近修改   : 
//  功能描述   : OLED 4接口演示例程(51系列)
//              说明: 
//              ----------------------------------------------------------------
//              GND    电源地
//              VCC  3.3v电源
//              SCL  P10（SCLK）
//              SDA  P11（MOSI）
//              RES  P12
//              DC   P13
//              CS   P14 
//              BLK  P15
//              ----------------------------------------------------------------
// 修改历史   :
// 日    期   : 
// 作    者   : HuangKai
// 修改内容   : 创建文件
//版权所有，盗版必究。
//Copyright(C) 中景园电子2014/3/16
//All rights reserved
//******************************************************************************/
#include "REG52.h"
#include "lcd_init.h"
#include "lcd.h"
#include "pic.h"
#include "intrins.h"
//sfr     P_SW1       =   0xa2;
sfr     P2M0        =   0x96;
sfr     P2M1        =   0x95;
sfr     P_SW1       =   0xa2;

unsigned int iii,ii;
bit shift;

/*void SPI_Isr() interrupt 9
{
    SPSTAT = 0xc0;                              //清中断标志
}*/

int main(void)
{
    float t;
    P_SW1 = 0x04;                               //SS_2/P2.2, MOSI_2/P2.3, MISO_2/P2.4, SCLK_2/P2.5
    P2M0=0xff;
    P2M1=0x00;
    LED=0;
//    P_SW1 = 0x04;              //SS_2/P2.2, MOSI_2/P2.3, MISO_2/P2.4, SCLK_2/P2.5

//    IE2 = ESPI;                                 //使能SPI中断
//    EA = 1;

    iii=0;ii=0;
    LED=1;
    t=0;
    SpiInt();
	LCD_Init();//LCD初始化
	LCD_Fill(0,0,LCD_W,LCD_H,WHITE);
	while(1)
	{
        iii=0;ii=0;
//		LCD_ShowChinese(0,0,"中景园电子",RED,WHITE,24,0);
//		LCD_ShowString(24,30,"LCD_W:",RED,WHITE,16,0);
//		LCD_ShowIntNum(72,30,LCD_W,3,RED,WHITE,16);
//		LCD_ShowString(24,50,"LCD_H:",RED,WHITE,16,0);
//		LCD_ShowIntNum(72,50,LCD_H,3,RED,WHITE,16);
//		LCD_ShowFloatNum1(20,80,t,4,RED,WHITE,16);
//		t+=0.11;
        for(iii=0;iii<5;iii++)
            {
            for(ii=0;ii<4;ii++)
		    {LCD_ShowPicture(32*ii,32*iii,32,32,gImage_baiyu);}
            }
        for(iii=0;iii<5;iii++)
            {
            for(ii=0;ii<4;ii++)
		    {LCD_ShowPicture(32*ii,32*iii,32,32,gImage_ff);}
            }
//		LCD_ShowPicture(0,65,40,64,gImage_FF);
//		LCD_ShowPicture(0,127,40,64,gImage_FF);
         LED=!LED;
	}
}

	