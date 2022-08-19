
#include "uart.h"

void delay(int d)
{
	while(d--);
}

int my_main()
{
	char c = 'A';
	
	while (1)
	{
		putchar(c++);
		delay(1000000);
		if (c == 'Z')
			c = 'A';
	}
	
	return 0;
}
