import zenoh
import json
import smbus
import time

from marcsrover.message import IMU

ADDRESS = 0x28  # adresse 7 bits du BNO055


class Node:
    def __init__(self):
        zenoh.init_log_from_env_or("info")

        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7446"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/0.0.0.0:0"])
        )
        self.zenoh_config.insert_json5("scouting/multicast/enabled", json.dumps(False))
        self.zenoh_config.insert_json5("scouting/gossip/enabled", json.dumps(True))

        PAGE_SWAP = 0x07
        ACC_CONF = 0x08
        GYR_CONF_0 = 0x0A
        GYR_CONF_1 = 0x0B
        MAG_CONF = 0x09
        TEMP_SOURCE = 0x40
        UNIT_SEL = 0x3B
        PWR_MODE = 0x3E
        HEADING = 0x1A
        MODE_REG = 0x3D
        FUSION_MODE = 0x0C

        # Initialisation du module
        self.i2cbus = smbus.SMBus(1)
        time.sleep(0.5)
        # data = self.i2cbus.read_i2c_block_data(ADDRESS, 0x3F, 1)
        # print(data[0])
        # data[0] = 0x20
        time.sleep(0.5)
        # i2cbus.write_byte_data(ADDRESS,0x3F,32)
        time.sleep(2)

        # A envoyer lors du premier test
        self.i2cbus.write_byte_data(ADDRESS, PAGE_SWAP, 1)
        self.i2cbus.write_byte_data(ADDRESS, ACC_CONF, 0x08)
        self.i2cbus.write_byte_data(ADDRESS, GYR_CONF_0, 0x23)
        self.i2cbus.write_byte_data(ADDRESS, GYR_CONF_1, 0x00)
        self.i2cbus.write_byte_data(ADDRESS, MAG_CONF, 0x1B)
        self.i2cbus.write_byte_data(ADDRESS, PAGE_SWAP, 0)
        self.i2cbus.write_byte_data(ADDRESS, TEMP_SOURCE, 0x01)
        self.i2cbus.write_byte_data(ADDRESS, UNIT_SEL, 0x01)
        self.i2cbus.write_byte_data(ADDRESS, PWR_MODE, 0x00)
        self.i2cbus.write_byte_data(ADDRESS, MODE_REG, FUSION_MODE)

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            imu = session.declare_publisher("marcsrover/imu")

            try:
                while True:
                    accel_x = self.i2cbus.read_word_data(ADDRESS, 0x08)
                    accel_y = self.i2cbus.read_word_data(ADDRESS, 0x0A)
                    accel_z = self.i2cbus.read_word_data(ADDRESS, 0x0C)
                    gyro_x = self.i2cbus.read_word_data(ADDRESS, 0x14)
                    gyro_y = self.i2cbus.read_word_data(ADDRESS, 0x16)
                    gyro_z = self.i2cbus.read_word_data(ADDRESS, 0x18)

                    bytes = IMU(
                        accel_x,
                        accel_y,
                        accel_z,
                        gyro_x,
                        gyro_y,
                        gyro_z,
                    ).serialize()

                    imu.put(bytes)

            except KeyboardInterrupt:
                print("Realsense received KeyboardInterrupt")

            imu.undeclare()
            session.close()

        print("Realsense node stopped")


def launch_node():
    node = Node()
    node.run()
