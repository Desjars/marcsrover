#include "tim.h"

#define NOTE_DO3 261.63
#define NOTE_RE3 293.66
#define NOTE_MI3 329.63
#define NOTE_FA3 349.23
#define NOTE_SOL3 392
#define NOTE_LA3 440
#define NOTE_SI3 493.88
#define NOTE_DO4 523.25

#define FREQ_TIMER_4 1000000 //1MHz

void buzzer_play(float frequency_Hz);

void buzzer_stop(void);
