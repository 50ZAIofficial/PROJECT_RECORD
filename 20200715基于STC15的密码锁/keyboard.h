
#ifndef __KEYBOARD_H__
#define __KEYBOARD_H__

#define key_state0  0   //״̬0����ʱ�ް�������
#define key_state1  1  	//״̬1����ʱ����ȷ�������Ƿ���
#define key_state2  2  	//״̬2����ʱ�жϰ����Ƿ��ͷ�
#define KEY P3			//������̵����ݿ�



#include <STC15F2K60S2.h>
#include <intrins.h>

extern bit KEYdatasending ;//���̵������Ƿ񱻶�ȡ��
extern unsigned char keydat;

extern unsigned char KEYstate;
unsigned char KEYscan();
void KEYinit();




#endif
