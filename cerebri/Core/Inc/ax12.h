#include "usart.h"

int AX12_set_goal(int degrees);
int AX12_write(int id, int start, int bytes, char* data);
void Dynamixel_SendPacket(uint8_t id, uint16_t address, uint32_t value, uint8_t data_length);
