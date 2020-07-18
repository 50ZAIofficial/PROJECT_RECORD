#include "DSP2833x_Device.h"     // DSP2833x Headerfile Include File
#include "DSP2833x_Examples.h"   // DSP2833x Examples Include File
#include "lcd_init.h"
#include "lcd.h"
#include "pic.h"

void spi_init()
{
    InitSpiaGpio();
    EALLOW;
    SysCtrlRegs.PCLKCR0.bit.SPIAENCLK = 1;   // SPI-A
    EDIS;
//  不使用FIFO
    SpiaRegs.SPICCR.all =0x0007;
            // 空闲时，CLK=1 Reset on, rising edge, 8-bit char bits
    SpiaRegs.SPICTL.all =0x000E;
    // Enable master mode, normal phase,
                                                  // enable talk, and SPI int disabled.
    SpiaRegs.SPIBRR =0x0000;                     //波特率 LSPCLK/(SPIBRR+1) 7.5M   LSPCLK=37.5M
    SpiaRegs.SPICCR.bit.SPISWRESET=1;         // Relinquish SPI from Reset
    SpiaRegs.SPIPRI.bit.FREE = 1;                // Set so breakpoints don't disturb xmission

}





/**
 * main.c
 */
int main(void)
{
    InitSysCtrl();
    LED_Init();
    spi_init();
    Lcd_Init();
    while(1)
    {
       // SPIx_ReadWriteByte(10);

        LCD_ShowPicture(0,0,40,40,gImage_baiyu);//显示图片
        LCD_Fill(0,0,128,160,RED);
        LCD_Fill(0,0,128,160,RED);
        LCD_Fill(0,0,128,160,RED);
   //     DELAY_US(100);
        LCD_Fill(0,0,128,160,WHITE);
        LCD_Fill(0,0,128,160,WHITE);
        LCD_Fill(0,0,128,160,WHITE);
    }
	return 0;
}

