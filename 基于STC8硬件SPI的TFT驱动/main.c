//////////////////////////////////////////////////////////////////////////////////	 
//������ֻ��ѧϰʹ�ã�δ��������ɣ��������������κ���;
//�о�԰����
//���̵�ַ��http://shop73023976.taobao.com/?spm=2013.1.0.0.M4PqC2
//
//  �� �� ��   : main.c
//  �� �� ��   : v2.0
//  ��    ��   : HuangKai
//  ��������   : 2014-0101
//  ����޸�   : 
//  ��������   : OLED 4�ӿ���ʾ����(51ϵ��)
//              ˵��: 
//              ----------------------------------------------------------------
//              GND    ��Դ��
//              VCC  3.3v��Դ
//              SCL  P10��SCLK��
//              SDA  P11��MOSI��
//              RES  P12
//              DC   P13
//              CS   P14 
//              BLK  P15
//              ----------------------------------------------------------------
// �޸���ʷ   :
// ��    ��   : 
// ��    ��   : HuangKai
// �޸�����   : �����ļ�
//��Ȩ���У�����ؾ���
//Copyright(C) �о�԰����2014/3/16
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
    SPSTAT = 0xc0;                              //���жϱ�־
}*/

int main(void)
{
    float t;
    P_SW1 = 0x04;                               //SS_2/P2.2, MOSI_2/P2.3, MISO_2/P2.4, SCLK_2/P2.5
    P2M0=0xff;
    P2M1=0x00;
    LED=0;
//    P_SW1 = 0x04;              //SS_2/P2.2, MOSI_2/P2.3, MISO_2/P2.4, SCLK_2/P2.5

//    IE2 = ESPI;                                 //ʹ��SPI�ж�
//    EA = 1;

    iii=0;ii=0;
    LED=1;
    t=0;
    SpiInt();
	LCD_Init();//LCD��ʼ��
	LCD_Fill(0,0,LCD_W,LCD_H,WHITE);
	while(1)
	{
        iii=0;ii=0;
//		LCD_ShowChinese(0,0,"�о�԰����",RED,WHITE,24,0);
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

	