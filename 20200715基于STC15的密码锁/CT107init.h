#ifndef _CT107INIT_H_
#define _CT107INIT_H_

#include <STC15F2K60S2.h>
#include <intrins.h>


sbit HC138_0=P2^5;
sbit HC138_1=P2^6;
sbit HC138_2=P2^7;

void HC138choose(unsigned char dat);
void CT107init();
void LEDbit(unsigned int LEDbiti);


#endif

