import zenoh
import json
import cv2

import pyrealsense2 as rs
import numpy as np

from marcsrover.message import D435I, IMU
from typing import Tuple


from marcsrover.common.realsense_depth import z16_to_XY8


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

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
        config.enable_stream(rs.stream.accel)
        config.enable_stream(rs.stream.gyro)

        # Start streaming
        self.pipeline.start(config)

    def get_frame(
        self,
    ) -> Tuple[
        bool, cv2.UMat | None, cv2.UMat | None, np.ndarray | None, np.ndarray | None
    ]:
        frames = self.pipeline.wait_for_frames()

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        accel_frame = frames[2].as_motion_frame().get_motion_data()
        gyro_frame = frames[3].as_motion_frame().get_motion_data()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        accel = np.array([accel_frame.x, accel_frame.y, accel_frame.z])
        gyro = np.array([gyro_frame.x, gyro_frame.y, gyro_frame.z])

        if not depth_frame or not color_frame or not accel_frame or not gyro_frame:
            return False, None, None, None, None

        return True, depth_image, color_image, accel, gyro

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            realsense = session.declare_publisher("marcsrover/realsense")
            imu = session.declare_publisher("marcsrover/imu")

            try:
                while True:
                    ret, depth_frame, color_frame, accel, gyro = self.get_frame()

                    if not ret:
                        continue

                    if (
                        color_frame is None
                        or depth_frame is None
                        or accel is None
                        or gyro is None
                    ):
                        continue

                    color_frame = cv2.resize(color_frame, (320, 240))
                    depth_frame = cv2.resize(depth_frame, (320, 240))

                    depth_frame = z16_to_XY8(depth_frame)

                    color_frame = cv2.imencode(
                        ".jpg", color_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60]
                    )[1].tobytes()

                    depth_frame = depth_frame.ravel().tobytes()

                    bytes = D435I(
                        rgb=color_frame,
                        depth=depth_frame,
                    ).serialize()

                    realsense.put(bytes)

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
                print("Realsense received KeyboardInterrupt")

            self.pipeline.stop()
            realsense.undeclare()
            imu.undeclare()
            session.close()

        print("Realsense node stopped")


def launch_node():
    node = Node()
    node.run()
