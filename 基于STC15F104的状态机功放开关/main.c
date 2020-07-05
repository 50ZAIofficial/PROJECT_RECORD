#include "reg52.h"
#include"intrins.h"

sfr P3M1 = 0xb1;
sfr P3M0 = 0xb2;
sbit P31=P3^1;
sbit P33=P3^3;
sbit P32=P3^2;
sbit INA=P3^5;
sbit INB=P3^4;
sbit RESET=P3^0;
bit warning;
bit first,final;

//-----------------------------------------
//��ʱ50ms
void Delay50ms()		//@6.000MHz
{
	unsigned char i, j, k;

	_nop_();
	_nop_();
	i = 2;
	j = 36;
	k = 206;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}

//-----------------------------------------
//��ʱ1000ms
void Delay1000ms()		//@6.000MHz
{
	unsigned char i, j, k;

	_nop_();
	_nop_();
	i = 23;
	j = 205;
	k = 120;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}

//-----------------------------------------
//�жϷ������
void exint0() interrupt 0       //INT0�ж����
{
    Delay50ms();
    if(P32==1) {first=1;P31=!P31;}
    else if(P32==0) {final=1;P31=!P31;}
}
//-----------------------------------------
//�жϷ������
void exint1() interrupt 2       //INT1�ж����
{
    Delay50ms();
    Delay50ms();
    if((P33==0)&&(P32==1))//�����Ǻ�ĵ�,ԭ����if(P33==0)
    {warning=1;P31=!P31;}//�����Կ�ȡ��
}
//-----------------------------------------
//�̵�������
void SwitchRelay()//����һ������������������رռ̵���
{    
    if(first==1){RESET=0;}
    Delay50ms();
    INA=!P32;
    INB=P32;//////////////////////////////////////////////
    Delay50ms();
    Delay50ms();
    Delay50ms();
    INA=0;
    INB=0;   //////////////////////////////////////////////
    if(first==1){Delay1000ms();RESET=1;first=0;}
    if(final==1) final=0;
}
//-----------------------------------------
//������
void warn()
{
    while(1)
    {
    if((P32==1)&&(warning==1)&&(P33==0))//����״̬�£��������жϣ������Ϊ��
        {
        RESET=0;
        Delay1000ms();
        Delay1000ms();
        Delay1000ms();
        RESET=1;
        Delay50ms();
        Delay50ms();
        }
   else
        {
        RESET=1;
        warning=0;
        break;
        }
    }
}
//-----------------------------------------
//���ų�ʼ��
void IntAMP()
{
    Delay50ms();//ǿ�ƹػ�һ��
    INA=1;
    INB=0;//////////////////////////////////////////////
    Delay50ms();
    Delay50ms();
    Delay50ms();
    INA=0;
    INB=0;   //////////////////////////////////////////////
    final=0;
}    

//-----------------------------------------
//�ж�״̬
int f(a,b,c,d)//a=P32,b=P33,c=first,d=final
{

    //��ֹ״̬
    if(a==0&&b==1&&d==0) //û�п����ź�ȴͨ�ŵ磬�쳣�Ŀ�������Ҫ�ػ�
    return 1;
    else if(a==1&&b==1)//�����Ĺػ�״̬��ʲôҲ����
    return 2;
    else if(a==0&&b==0)//�����Ŀ���״̬��ʲôҲ����
    return 3;

    //����״̬
    else if(a==1&&b==0&&c==0)//���о����Ŀ���״̬����warn���������п����ź�ȴû�������̵�������
    return 4;
    else if(a==1&&b==0&&c==1)//����
    return 5;
    else if(a==0&&b==1&&d==1)//�ػ�
    return 6;
    else return 0;
}
//-----------------------------------------

//-----------------------------------------
void main()
{
    INA=0;
    INB=0;//�ϵ�������õͣ���ֹ�����
    P31=1;
    P32=1;
    P33=1;
    P3M0 = 0x00;
    P3M1 = 00000100;//P33��P32����Ϊ����̬
//    P3M1 = 0x00;
    INT1 = 1;
    IT1 = 1;                    //����INT1���ж����� (1:���½��� 0:�����غ��½���)
    EX1 = 1;                    //ʹ��INT1�ж�

    INT0 = 1;
    IT0 = 0;                    //����INT0���ж����� (1:���½��� 0:�����غ��½���)
    EX0 = 1;                    //ʹ��INT0�ж�

    EA = 1;

    RESET=1;

    first=0;
    warning=0;

    IntAMP();

    for(;;)
    {
        switch(f(P32,P33,first,final))
        {
            case 1:IntAMP();Delay1000ms();break;
            case 2:_nop_();break;
            case 3:_nop_();break;
            case 4:SwitchRelay();warn();Delay1000ms();break;
            case 5:SwitchRelay();break;
            case 6:SwitchRelay();warning=0;break;
            default:IntAMP();Delay1000ms();break;
        }
    }
}
