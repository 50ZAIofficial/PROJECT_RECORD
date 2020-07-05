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
//延时50ms
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
//延时1000ms
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
//中断服务程序
void exint0() interrupt 0       //INT0中断入口
{
    Delay50ms();
    if(P32==1) {first=1;P31=!P31;}
    else if(P32==0) {final=1;P31=!P31;}
}
//-----------------------------------------
//中断服务程序
void exint1() interrupt 2       //INT1中断入口
{
    Delay50ms();
    Delay50ms();
    if((P33==0)&&(P32==1))//这里是后改的,原来是if(P33==0)
    {warning=1;P31=!P31;}//将测试口取反
}
//-----------------------------------------
//继电器操作
void SwitchRelay()//发射一个短脉冲用来开启或关闭继电器
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
//报错检测
void warn()
{
    while(1)
    {
    if((P32==1)&&(warning==1)&&(P33==0))//开机状态下，触发过中断，报错脚为低
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
//功放初始化
void IntAMP()
{
    Delay50ms();//强制关机一次
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
//判断状态
int f(a,b,c,d)//a=P32,b=P33,c=first,d=final
{

    //静止状态
    if(a==0&&b==1&&d==0) //没有开机信号却通着电，异常的开机，需要关机
    return 1;
    else if(a==1&&b==1)//正常的关机状态，什么也不做
    return 2;
    else if(a==0&&b==0)//正常的开机状态，什么也不做
    return 3;

    //动作状态
    else if(a==1&&b==0&&c==0)//带有警报的开机状态，进warn。或者是有开机信号却没开机，继电器动作
    return 4;
    else if(a==1&&b==0&&c==1)//开机
    return 5;
    else if(a==0&&b==1&&d==1)//关机
    return 6;
    else return 0;
}
//-----------------------------------------

//-----------------------------------------
void main()
{
    INA=0;
    INB=0;//上电后立刻置低，防止误操作
    P31=1;
    P32=1;
    P33=1;
    P3M0 = 0x00;
    P3M1 = 00000100;//P33和P32设置为高阻态
//    P3M1 = 0x00;
    INT1 = 1;
    IT1 = 1;                    //设置INT1的中断类型 (1:仅下降沿 0:上升沿和下降沿)
    EX1 = 1;                    //使能INT1中断

    INT0 = 1;
    IT0 = 0;                    //设置INT0的中断类型 (1:仅下降沿 0:上升沿和下降沿)
    EX0 = 1;                    //使能INT0中断

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
