#include "DSP2833x_Device.h"     // DSP2833x Headerfile Include File
#include"math.h"

//滤波器参数
#define NZEROS 4
#define NPOLES 4
#define GAIN   3.836492796e+06

static float xv[NZEROS+1], yv[NPOLES+1];

//输入信号参数
#define SIGNAL1F 3906.25‬
#define PI 3.1415926

//定义函数
float InputWave();
float Trianglewave();
int Compare();
float filterloop();
void shiftPWM();
void dif();
void DeadTime(DT);

unsigned int SavePWM[16];
unsigned int shiftteamI,shiftI;
void INTshiftPWM();


float ftng,fn;
float fInput,fOutput,fCompare;
float fSignal1;
float fStepSignal1;
float f2PI;
int bit;
float fIn[256],fCp[256],fOut[256];
int nIn,Ntng,PWMoneCLK,Cp;
int PWMout[256];
int difPWMout[256];//差分输出推动半桥


void main()
{
 //   InitSysCtrl();
    INTshiftPWM();
    nIn=0;
    f2PI=2*PI;
    Ntng=1;
    bit=1;
    fSignal1=0.0;
    fStepSignal1=2*PI/256;
    shiftteamI=0;
    shiftI=0;
    for(;;)
    {
        fCompare=Trianglewave();
        fCp[nIn]=fCompare;//观察三角波

        fInput=InputWave();
        fIn[nIn]=fInput;//观察正弦波

        Cp=Compare();
        PWMout[nIn]=Cp;

        shiftPWM();

        fOut[nIn]=filterloop();

        nIn++;

        if(nIn==256)
        {
            nIn=0;
            dif();
            DeadTime(5);

        }
    }

}


float InputWave()
{
    fn=sin(fSignal1)+1;
    fSignal1+=fStepSignal1;
    if ( fSignal1>=f2PI )  fSignal1-=f2PI;
    return(fn);
}

float Trianglewave()
{
    ftng=0.65*Ntng-0.3;
    if ( Ntng==4)   {bit=0;}//此时N--
    if ( Ntng==0)   {bit=1;}//此时N++
    switch(bit)
    {
        case 0:Ntng--;
        break;
        case 1:Ntng++;
        break;
        default:break;
    }
    return(ftng);
}

int Compare()
{
    if(fCompare>=fInput)PWMoneCLK=0;
    else PWMoneCLK=1;
    return(PWMoneCLK);
}


float filterloop()
  {
        xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4];
        xv[4] = Cp/GAIN;
        yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4];
        yv[4] =   (xv[0] + xv[4]) + 4 * (xv[1] + xv[3]) + 6 * xv[2]
                     + ( -0.9418920323 * yv[0]) + (  3.8201946290 * yv[1])
                     + ( -5.8145385566 * yv[2]) + (  3.9362317895 * yv[3]);
        return(yv[4]);

  }
void INTshiftPWM()
{
    shiftteamI=0;
    shiftI=0;
    int iii;
    unsigned int maxint=65535;
    for(iii=0;iii<=32;iii++){SavePWM[iii]=maxint;}
}
void shiftPWM()
{
    shiftI++;
    unsigned int Dat;
    Dat=Cp;
    SavePWM[shiftteamI]=SavePWM[shiftteamI]|Dat;
    SavePWM[shiftteamI]=SavePWM[shiftteamI]<<1;
    if(shiftI>15){shiftteamI++;shiftI=0;}
}

void dif()
{
    unsigned int ii;
    for(ii=0;ii!=256;ii++)
    {difPWMout[ii]=PWMout[ii];difPWMout[ii]=!difPWMout[ii];}//比较完成后，生成差分输出
}

void DeadTime(DT)
{
    int ii,iii;
    for(ii=DT;ii<512;ii++)
    {
    if(PWMout[ii]==0&&PWMout[ii+1]==1)
        {for(iii=1;iii<DT+1;iii++){ PWMout[ii+iii]=0;}}
    if(PWMout[ii]==1&&PWMout[ii+1]==0)
        {for(iii=1;iii<DT+1;iii++){difPWMout[ii+iii]=0;}}
    }
}
