#include "main.h"
#include "tim.h"
#include "motor.h"
#include "usart.h"

#define Kp 0.2

#define Ti 0.2

#define Te 20e-3

#define MAX_BUFFER_SIZE 100

void init_serial();
void processMessage(uint8_t *message);
