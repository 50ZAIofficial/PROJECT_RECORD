#include <password.h>

unsigned char PASSWORDbit=0;
unsigned char PASSWORDtruebit=0;
unsigned char Pbit[6]={0,0,0,0,0,0};

void PASSWORDinit(unsigned char Pbit1,unsigned char Pbit2,unsigned char Pbit3,
unsigned char Pbit4,unsigned char Pbit5,unsigned char Pbit6)
{ 
    PASSWORDbit=0;
    PASSWORDtruebit=0;
    KEYdatasending=0;
    Pbit[0]=Pbit1;
    Pbit[1]=Pbit2;
    Pbit[2]=Pbit3;
    Pbit[3]=Pbit4;
    Pbit[4]=Pbit5;
    Pbit[5]=Pbit6;
}

unsigned char PASSWORDcompareresult()
{
    if(PASSWORDtruebit==7){PASSWORDtruebit=0;}
    switch(PASSWORDbit)
    {
        case 0:PASSWORDtruebit=0;break;
        case 1:if(keydat==Pbit[0]){if(KEYdatasending==1){PASSWORDtruebit++;KEYdatasending=0;}}break;
        case 2:if(keydat==Pbit[1]){if(KEYdatasending==1){PASSWORDtruebit++;KEYdatasending=0;}}break;
        case 3:if(keydat==Pbit[2]){if(KEYdatasending==1){PASSWORDtruebit++;KEYdatasending=0;}}break;
        case 4:if(keydat==Pbit[3]){if(KEYdatasending==1){PASSWORDtruebit++;KEYdatasending=0;}}break;
        case 5:if(keydat==Pbit[4]){if(KEYdatasending==1){PASSWORDtruebit++;KEYdatasending=0;}}break;
        case 6:if(keydat==Pbit[5]){if(KEYdatasending==1){PASSWORDtruebit++;KEYdatasending=0;}}break;
    }
//    if(PASSWORDtruebit==5){return 1;}
//    else {return 0;}
    if(KEYdatasending==0){return 15;}
    return PASSWORDtruebit;
}





