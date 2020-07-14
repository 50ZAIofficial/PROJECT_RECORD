#include "STC15F2K60S2.h"	
#include <intrins.h>
#include <smg.h>
#include <CT107init.h>

unsigned char code SMG_duanma[18]=
{0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0x88,0x80,0xc6,0xc0,0x86,0x8e,
0xbf,0x7f};

void SMGdelay(unsigned int t)
{
    while(t--);
}

void SMGinit()
{
    HC138choose(6);
    P0=0x00;
    HC138choose(7);
    P0=SMG_duanma[0];
}
void SMGbit(unsigned char dat,unsigned char smgbit)
{
    HC138choose(6);
    P0= 0x01 << smgbit;
    HC138choose(7);
    P0= SMG_duanma[dat];
}
void SGMdynamic(unsigned char dat0,unsigned char dat1,
unsigned char dat2,unsigned char dat3,
unsigned char dat4,unsigned char dat5,
unsigned char dat6,unsigned char dat7)
{
    SMGdelay(1000);
    SMGbit(dat0,0);
    SMGdelay(1000);
    SMGbit(dat1,1);
    SMGdelay(1000);
    SMGbit(dat2,2);
    SMGdelay(1000);
    SMGbit(dat3,3);
    SMGdelay(1000);
    SMGbit(dat4,4);
    SMGdelay(1000);
    SMGbit(dat5,5);
    SMGdelay(1000);
    SMGbit(dat6,6);
    SMGdelay(1000);
    SMGbit(dat7,7);
}

unsigned char SMGbitdata(unsigned char nowbiti,unsigned char biti,unsigned char datai)
{
   if(biti==nowbiti){return datai;}
   else {return 15;}
}