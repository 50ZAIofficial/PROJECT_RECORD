#ifndef _SMG_H_
#define _SMG_H_

#include <STC15F2K60S2.h>
#include <intrins.h>


void SMGbit(unsigned char dat,unsigned char smgbit);
void SMGinit();
void SGMdynamic(unsigned char dat0,unsigned char dat1,
unsigned char dat2,unsigned char dat3,unsigned char dat4,
unsigned char dat5,unsigned char dat6,unsigned char dat7);
unsigned char SMGbitdata(unsigned char nowbiti,unsigned char biti,unsigned char datai);


#endif
