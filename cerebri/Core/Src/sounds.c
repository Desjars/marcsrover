#include <sounds.h>

void buzzer_play(float frequency_Hz){
	HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);

	uint32_t period = FREQ_TIMER_4 / frequency_Hz;

	htim4.Instance->ARR = period + 1;

	__HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_1, period / 2);
}

void buzzer_stop(void){
	HAL_TIM_PWM_Stop(&htim4, TIM_CHANNEL_1);
}
