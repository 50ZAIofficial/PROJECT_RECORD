#include <CT107init.h>
#include "STC15F2K60S2.h"	
#include <intrins.h>

void CT107init()
{
    HC138choose(5);
    P06=0;//·äÃùÆ÷
    P04=0;//¼ÌµçÆ÷
    HC138choose(4);
    P0=0xff;
}
void HC138choose(unsigned char dat)
{
    switch (dat)
    {
        case 0 : HC138_0=0;HC138_1=0;HC138_2=0;break;
        case 1 : HC138_0=1;HC138_1=0;HC138_2=0;break;
        case 2 : HC138_0=0;HC138_1=1;HC138_2=0;break;
        case 3 : HC138_0=1;HC138_1=1;HC138_2=0;break;
        case 4 : HC138_0=0;HC138_1=0;HC138_2=1;break;
        case 5 : HC138_0=1;HC138_1=0;HC138_2=1;break;
        case 6 : HC138_0=0;HC138_1=1;HC138_2=1;break;
        case 7 : HC138_0=1;HC138_1=1;HC138_2=1;break;
    }
}

void LEDbit(unsigned int LEDbiti)
{
    HC138choose(4);
    P0=LEDbiti;
}