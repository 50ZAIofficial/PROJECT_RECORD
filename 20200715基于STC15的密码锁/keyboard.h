
#ifndef __KEYBOARD_H__
#define __KEYBOARD_H__

#define key_state0  0   //状态0，此时无按键按下
#define key_state1  1  	//状态1，此时处于确定按键是否按下
#define key_state2  2  	//状态2，此时判断按键是否释放
#define KEY P3			//矩阵键盘的数据口



#include <STC15F2K60S2.h>
#include <intrins.h>

extern bit KEYdatasending ;//键盘的数据是否被读取了
extern unsigned char keydat;

extern unsigned char KEYstate;
unsigned char KEYscan();
void KEYinit();




#endif
