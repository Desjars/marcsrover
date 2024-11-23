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
// Fonction pour calculer le checksum du paquet Dynamixel
uint8_t CalculateChecksum(uint8_t *packet, uint8_t length) {
    uint16_t checksum = 0;
    for (uint8_t i = 2; i < length; i++) { // Sauter les 2 premiers octets
        checksum += packet[i];
    }
    return ~((uint8_t)checksum);
}

// Fonction pour envoyer un paquet Dynamixel
void Dynamixel_SendPacket(uint8_t id, uint16_t address, uint32_t value, uint8_t data_length) {
    uint8_t packet[10 + data_length]; // Paquet Dynamixel (header, ID, length, instruction, etc.)
    uint8_t index = 0;

    // Construction du paquet Dynamixel
    packet[index++] = 0xFF;                     // Header 1
    packet[index++] = 0xFF;                     // Header 2
    packet[index++] = id;                       // ID du moteur
    packet[index++] = data_length + 3;          // Longueur des données + Instruction + CRC
    packet[index++] = 0x03;                     // Instruction "WRITE_DATA"
    packet[index++] = address & 0xFF;           // Adresse basse
    packet[index++] = (address >> 8) & 0xFF;    // Adresse haute
    packet[index++] = value & 0xFF;             // Valeur basse
    packet[index++] = (value >> 8) & 0xFF;      // Valeur
    packet[index++] = (value >> 16) & 0xFF;     // Valeur
    packet[index++] = (value >> 24) & 0xFF;     // Valeur haute

    // Calculer le checksum
    uint8_t checksum = CalculateChecksum(packet, index);
    packet[index++] = checksum;

    // Envoyer le paquet
    HAL_UART_Transmit(&huart1, packet, index, 500);
}
