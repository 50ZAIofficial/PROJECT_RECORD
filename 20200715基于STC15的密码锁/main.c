#include "STC15F2K60S2.h"	
#include <intrins.h>
#include <CT107init.h>
#include <smg.h>
#include <keyboard.h>
#include <password.h>

void PASSWORDresetKEY(unsigned char ii);

unsigned char i=0;
unsigned char keydat;
unsigned char PandB[7]={0,0,0,0,0,0,0};


void t2int() interrupt 12           //中断入口
{
  keydat=KEYscan();
  IE2 &= ~0x04;                   //若需要手动清除中断标志,可先关闭中断,此时系统会自动清除内部的中断标志
  IE2 |= 0x04;                    //然后再开中断即可
//  keydat=1;
  if(KEYstate==1){PASSWORDbit++;KEYdatasending=1;}
}

void Timer2Init(void)		//10毫秒@22.1184MHz
{
	AUXR &= 0xFB;		//定时器时钟12T模式
	T2L = 0x00;		//设置定时初值
	T2H = 0xB8;		//设置定时初值
	AUXR |= 0x10;		//定时器2开始计时

    IE2 |= 0x04;                    //开定时器2中断
    EA = 1;

    keydat=0;
}



void MAINdelay(unsigned int t)
{
    while(t--);
}

void main()
{
    unsigned char ii;
    PASSWORDinit(1,1,4,5,1,4);
    Timer2Init();
    P3M0 = 0x00;
    P3M1 = 0x00;
    CT107init();
    SMGinit();
    LEDbit(0xff);
    while(1)
    {
    i=PASSWORDcompareresult();
    PandB[PASSWORDbit]=keydat;
    SGMdynamic(16,16,PandB[1],PandB[2],PandB[3],PandB[4],PandB[5],PandB[6]);

    if(PASSWORDbit==6&&PASSWORDtruebit==6)
        {LEDbit(0x00);}
    else{LEDbit(0xff);}


    PASSWORDresetKEY(15);


    if(PASSWORDtruebit>=7){PASSWORDtruebit=0;}
    if(PASSWORDbit>=7){PASSWORDbit=1;PASSWORDtruebit=0;}
    }
}


void PASSWORDresetKEY(unsigned char ii)
{
    if(ii==keydat)
    {
        keydat=0;PASSWORDbit=1;PASSWORDtruebit=0;
        for(ii=0;ii<=6;ii++){PandB[ii]=0;}
    }
}
