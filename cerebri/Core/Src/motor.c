#include "motor.h"

void send_normalized_cmd(float cmd)
{
	uint32_t dc; //min 1560 et max 1720

	if (cmd == 0.0)
	{
		dc = 1500;
	} else if (cmd > 0.0)
	{
		dc = 1560 + cmd * (1720 - 1560);
	} else if (cmd < 0.0)
	{
		dc = 1440 + cmd * (1720 - 1560);
	}

	dc = dc < 1000?1000:dc;
	dc = dc > 2000?2000:dc;

	__HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, dc);
}
