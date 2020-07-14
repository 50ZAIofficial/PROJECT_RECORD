#include <keyboard.h>

unsigned char KEYstate=0;
bit KEYdatasending=0;
//键盘返回值

unsigned char KEYscan()
{
    unsigned char KEYc,KEYr,KEYp4;
    unsigned char KEYvalue,KEYbit;
//state0未按下，1按下，2判断完，检测是否放开
    KEY=0xf0;
    P42=1;P44=1;
    KEYr=KEY;
    KEYp4=P44;
    KEYp4=KEYp4<<1;
    KEYp4=KEYp4|P42;
    KEYp4=KEYp4<<6;
    KEYp4=KEYp4|0x3f;
    KEYr=KEY&0xf0;
    KEYr=KEYr&KEYp4;

    KEY=0x0f;
    P42=0;P44=0;
    KEYc=KEY;
    KEYc=KEY&0x0f;
    KEYbit=KEYr|KEYc;

    switch(KEYstate)
    {
        case key_state0:
            if(KEYbit!=0xff)
            {KEYstate=key_state1;}break;
        case key_state1:
            if(KEYbit==0xff)
            {KEYstate=key_state0;}
            else
            {
                switch(KEYbit)
                {	 case 0xee: KEYvalue=0;break;
				     case 0xde: KEYvalue=1;break;
				     case 0xbe: KEYvalue=2;break;
				     case 0x7e: KEYvalue=3;break;
				     case 0xed: KEYvalue=4;break;
				     case 0xdd: KEYvalue=5;break;
				     case 0xbd: KEYvalue=6;break;
				     case 0x7d: KEYvalue=7;break;
				     case 0xeb: KEYvalue=8;break;
				     case 0xdb: KEYvalue=9;break;
				     case 0xbb: KEYvalue=10;break;
				     case 0x7b: KEYvalue=11;break;
				     case 0xe7: KEYvalue=12;break;
				     case 0xd7: KEYvalue=13;break;
				     case 0xb7: KEYvalue=14;break;
				     case 0x77: KEYvalue=15;break;
                }
            KEYstate=key_state2;
            }
        break;
        case key_state2:
            if(KEYbit==0xff)
            {KEYstate=key_state0;}
        break;
    }
    return KEYvalue;
}