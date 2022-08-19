
#include "uart.h"

void delay(int d)
{
	while(d--);
}

int main()
{
	unsigned int *p = (unsigned int *)0x08040004;
	unsigned int val = *p;  /* get the 2nd item from app's vector */
	
	void (*app)(void);
	
	uart_init();

	putstr("bootloader\r\n");
	
	/* start app */
	app = (void (*)(void))val;  
	
	app();
	
	return 0;
}
