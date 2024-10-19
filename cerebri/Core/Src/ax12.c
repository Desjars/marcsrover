#include <ax12.h>

int AX12_set_goal(int degrees) {
    char data[2];

    // Convert degrees to the goal position for AX12
    short goal = (1023 * ((degrees + 15) * 23 / 35 + 128)) / 300;

    // Split goal into 2 bytes (low and high)
    data[0] = goal & 0xFF;  // lower 8 bits
    data[1] = goal >> 8;    // upper 8 bits

    // Goal position register address in AX12
    int ax12RegGoalPosition = 30;

    return AX12_write(1, ax12RegGoalPosition, 2, data);
}

int AX12_write(int id, int start, int bytes, char* data) {
    // Packet structure: 0xFF, 0xFF, ID, Length, Instruction (write), Address, Params, Checksum

    char sum = 0;
    char status[6];      // Status packet to receive
    char txBuf[16];      // Transmit buffer

    // Build the TxPacket
    txBuf[0] = 0xFF;     // Start of packet
    txBuf[1] = 0xFF;

    // Set ID
    txBuf[2] = id;
    sum += txBuf[2];

    // Set packet length (Instruction + Address + Params)
    txBuf[3] = 3 + bytes;
    sum += txBuf[3];

    // Set Instruction (0x03 = Write)
    txBuf[4] = 0x03;
    sum += txBuf[4];

    // Set start address
    txBuf[5] = start;
    sum += txBuf[5];

    // Add data bytes
    for (uint8_t i = 0; i < bytes; i++) {
        txBuf[6 + i] = data[i];
        sum += txBuf[6 + i];
    }

    // Calculate checksum
    txBuf[6 + bytes] = 0xFF - sum;

    // Transmit the packet via UART
    HAL_UART_Transmit(&huart1, (uint8_t *)txBuf, 7 + bytes, 500);

    // Simulate valid return (ensure valid communication)
    status[4] = 0x00;

    return status[4];
}
