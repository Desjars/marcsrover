import zenoh
import json

import pyrealsense2 as rs
import numpy as np

from marcsrover.message import IMU
from typing import Tuple


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

        self.pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.accel)
        config.enable_stream(rs.stream.gyro)

        # Start streaming
        self.pipeline.start(config)

    def get_frame(
        self,
    ) -> Tuple[bool, np.ndarray | None, np.ndarray | None]:
        frames = self.pipeline.wait_for_frames()

        accel_frame = frames[0].as_motion_frame().get_motion_data()
        gyro_frame = frames[1].as_motion_frame().get_motion_data()

        accel = np.array([accel_frame.x, accel_frame.y, accel_frame.z])
        gyro = np.array([gyro_frame.x, gyro_frame.y, gyro_frame.z])

        if not accel_frame or not gyro_frame:
            return False, None, None

        return True, accel, gyro

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            imu = session.declare_publisher("marcsrover/imu")

            try:
                while True:
                    ret, accel, gyro = self.get_frame()

                    if not ret:
                        continue

                    if accel is None or gyro is None:
                        continue

                    bytes = IMU(
                        accel_x=accel[0],
                        accel_y=accel[1],
                        accel_z=accel[2],
                        gyro_x=gyro[0],
                        gyro_y=gyro[1],
                        gyro_z=gyro[2],
                    ).serialize()

                    imu.put(bytes)

            except KeyboardInterrupt:
                print("Realsense IMU received KeyboardInterrupt")

            self.pipeline.stop()
            imu.undeclare()
            session.close()

        print("Realsense IMU node stopped")


def launch_node():
    node = Node()
    node.run()
