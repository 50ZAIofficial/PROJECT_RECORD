#ifndef __PASSWORD_H__
#define __PASSWORD_H__



#include "STC15F2K60S2.h"	
#include <intrins.h>
#include <keyboard.h>

extern unsigned char PASSWORDbit;
extern unsigned char PASSWORDtruebit;
extern unsigned char Pbit[6];

void PASSWORDinit(unsigned char Pbit1,unsigned char Pbit2,unsigned char Pbit3,
unsigned char Pbit4,unsigned char Pbit5,unsigned char Pbit6);
unsigned char PASSWORDcompareresult();


#endif