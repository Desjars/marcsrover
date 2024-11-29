import enum

import numpy as np

from typing import Union, Tuple

from dynamixel_sdk import (
    PacketHandler,
    PortHandler,
    COMM_SUCCESS,
)

PROTOCOL_VERSION = 2.0
BAUD_RATE = 1_000_000
TIMEOUT_MS = 1000


class TorqueMode(enum.Enum):
    ENABLED = np.uint32(1)
    DISABLED = np.uint32(0)


class OperatingMode(enum.Enum):
    VELOCITY = np.uint32(1)
    POSITION = np.uint32(3)
    EXTENDED_POSITION = np.uint32(4)
    CURRENT_CONTROLLED_POSITION = np.uint32(5)
    PWM = np.uint32(16)


X_SERIES_CONTROL_TABLE = [
    ("Model_Number", 0, 2),
    ("Model_Information", 2, 4),
    ("Firmware_Version", 6, 1),
    ("ID", 7, 1),
    ("Baud_Rate", 8, 1),
    ("Return_Delay_Time", 9, 1),
    ("Drive_Mode", 10, 1),
    ("Operating_Mode", 11, 1),
    ("Secondary_ID", 12, 1),
    ("Protocol_Type", 13, 1),
    ("Homing_Offset", 20, 4),
    ("Moving_Threshold", 24, 4),
    ("Temperature_Limit", 31, 1),
    ("Max_Voltage_Limit", 32, 2),
    ("Min_Voltage_Limit", 34, 2),
    ("PWM_Limit", 36, 2),
    ("Current_Limit", 38, 2),
    ("Acceleration_Limit", 40, 4),
    ("Velocity_Limit", 44, 4),
    ("Max_Position_Limit", 48, 4),
    ("Min_Position_Limit", 52, 4),
    ("Shutdown", 63, 1),
    ("Torque_Enable", 64, 1),
    ("LED", 65, 1),
    ("Status_Return_Level", 68, 1),
    ("Registered_Instruction", 69, 1),
    ("Hardware_Error_Status", 70, 1),
    ("Velocity_I_Gain", 76, 2),
    ("Velocity_P_Gain", 78, 2),
    ("Position_D_Gain", 80, 2),
    ("Position_I_Gain", 82, 2),
    ("Position_P_Gain", 84, 2),
    ("Feedforward_2nd_Gain", 88, 2),
    ("Feedforward_1st_Gain", 90, 2),
    ("Bus_Watchdog", 98, 1),
    ("Goal_PWM", 100, 2),
    ("Goal_Current", 102, 2),
    ("Goal_Velocity", 104, 4),
    ("Profile_Acceleration", 108, 4),
    ("Profile_Velocity", 112, 4),
    ("Goal_Position", 116, 4),
    ("Realtime_Tick", 120, 2),
    ("Moving", 122, 1),
    ("Moving_Status", 123, 1),
    ("Present_PWM", 124, 2),
    ("Present_Current", 126, 2),
    ("Present_Velocity", 128, 4),
    ("Present_Position", 132, 4),
    ("Velocity_Trajectory", 136, 4),
    ("Position_Trajectory", 140, 4),
    ("Present_Input_Voltage", 144, 2),
    ("Present_Temperature", 146, 1),
]

MODEL_CONTROL_TABLE = {
    "x_series": X_SERIES_CONTROL_TABLE,
    "xl330-m077": X_SERIES_CONTROL_TABLE,
    "xl330-m288": X_SERIES_CONTROL_TABLE,
    "xl430-w250": X_SERIES_CONTROL_TABLE,
    "xm430-w350": X_SERIES_CONTROL_TABLE,
    "xm540-w270": X_SERIES_CONTROL_TABLE,
}


class DynamixelBus:
    def __init__(self, port: str, description: dict[str, Tuple[int, str]]):
        self.port = port
        self.descriptions = description
        self.motor_ctrl = {}

        for motor_name, (motor_id, motor_model) in description.items():
            if motor_model not in MODEL_CONTROL_TABLE:
                raise ValueError(f"Model {motor_model} is not supported.")

            self.motor_ctrl[motor_name] = {}

            self.motor_ctrl[motor_name]["id"] = motor_id
            for data_name, address, bytes_size in MODEL_CONTROL_TABLE[motor_model]:
                self.motor_ctrl[motor_name][data_name] = {
                    "addr": address,
                    "bytes_size": bytes_size,
                }

        self.port_handler = PortHandler(self.port)
        self.packet_handler = PacketHandler(PROTOCOL_VERSION)

        if not self.port_handler.openPort():
            raise OSError(f"Failed to open port {self.port}")

        self.port_handler.setBaudRate(BAUD_RATE)
        self.port_handler.setPacketTimeoutMillis(TIMEOUT_MS)

        self.group_readers = {}
        self.group_writers = {}

    def close(self):
        self.port_handler.closePort()

    def write(
        self, data_name: str, value: Union[np.uint32, np.int32, None], motor_name: str
    ):
        if value is None:
            return

        value = value.astype(np.uint32)

        motor_id = self.motor_ctrl[motor_name]["id"]
        packet_address = self.motor_ctrl[motor_name][data_name]["addr"]
        packet_bytes_size = self.motor_ctrl[motor_name][data_name]["bytes_size"]

        args = (self.port_handler, motor_id, packet_address, value)

        if packet_bytes_size == 1:
            comm, err = self.packet_handler.write1ByteTxRx(*args)
        elif packet_bytes_size == 2:
            comm, err = self.packet_handler.write2ByteTxRx(*args)
        elif packet_bytes_size == 4:
            comm, err = self.packet_handler.write4ByteTxRx(*args)
        else:
            raise NotImplementedError(
                f"Value of the number of bytes to be sent is expected to be in [1, 2, 4], but {packet_bytes_size} "
                f"is provided instead."
            )

        if comm != COMM_SUCCESS:
            raise ConnectionError(
                f"Write failed due to communication error on port {self.port} for motor {motor_id}: "
                f"{self.packet_handler.getTxRxResult(comm)}"
            )
        elif err != 0:
            raise ConnectionError(
                f"Write failed due to error {err} on port {self.port} for motor {motor_id}: "
                f"{self.packet_handler.getTxRxResult(err)}"
            )

    def read(self, data_name: str, motor_name: str) -> np.int32:
        motor_id = self.motor_ctrl[motor_name]["id"]
        packet_address = self.motor_ctrl[motor_name][data_name]["addr"]
        packet_bytes_size = self.motor_ctrl[motor_name][data_name]["bytes_size"]

        args = (self.port_handler, motor_id, packet_address)
        if packet_bytes_size == 1:
            value, comm, err = self.packet_handler.read1ByteTxRx(*args)
        elif packet_bytes_size == 2:
            value, comm, err = self.packet_handler.read2ByteTxRx(*args)
        elif packet_bytes_size == 4:
            value, comm, err = self.packet_handler.read4ByteTxRx(*args)
        else:
            raise NotImplementedError(
                f"Value of the number of bytes to be sent is expected to be in [1, 2, 4], but "
                f"{packet_bytes_size} is provided instead."
            )

        if comm != COMM_SUCCESS:
            raise ConnectionError(
                f"Read failed due to communication error on port {self.port} for motor {motor_id}: "
                f"{self.packet_handler.getTxRxResult(comm)}"
            )
        elif err != 0:
            raise ConnectionError(
                f"Read failed due to error {err} on port {self.port} for motor {motor_id}: "
                f"{self.packet_handler.getTxRxResult(err)}"
            )

        return np.uint32(value).astype(np.int32)

    def write_torque_enable(self, torque_mode: TorqueMode, motor_name: str):
        self.write("Torque_Enable", torque_mode.value, motor_name)

    def write_operating_mode(self, operating_mode: OperatingMode, motor_name: str):
        self.write("Operating_Mode", operating_mode.value, motor_name)

    def read_position(self, motor_name: str) -> np.int32:
        return self.read("Present_Position", motor_name)

    def read_velocity(self, motor_name: str) -> np.int32:
        return self.read("Present_Velocity", motor_name)

    def read_current(self, motor_name: str) -> np.int32:
        return self.read("Present_Current", motor_name)

    def write_goal_position(
        self, goal_position: Union[np.int32, np.uint32], motor_name: str
    ):
        self.write("Goal_Position", goal_position, motor_name)

    def write_goal_current(
        self, goal_current: Union[np.int32, np.uint32], motor_name: str
    ):
        self.write("Goal_Current", goal_current, motor_name)

    def write_position_p_gain(
        self, position_p_gain: Union[np.int32, np.uint32], motor_name: str
    ):
        self.write("Position_P_Gain", position_p_gain, motor_name)

    def write_position_i_gain(
        self, position_i_gain: Union[np.int32, np.uint32], motor_name: str
    ):
        self.write("Position_I_Gain", position_i_gain, motor_name)

    def write_position_d_gain(
        self, position_d_gain: Union[np.int32, np.uint32], motor_name: str
    ):
        self.write("Position_D_Gain", position_d_gain, motor_name)
