import zenoh
import json

import numpy as np
import cv2

from vehicle import Driver
from controller import Lidar, Camera, RangeFinder

from dataclasses import dataclass

from pycdr2 import IdlStruct
from pycdr2.types import float32
from typing import List


@dataclass
class OpenCVCamera(IdlStruct):
    frame: bytes


@dataclass
class LidarScan(IdlStruct):
    qualities: List[float32]
    angles: List[float32]
    distances: List[float32]


class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7447"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/127.0.0.1:0"])
        )
        self.zenoh_config.insert_json5("scouting/multicast/enabled", json.dumps(False))

        self.driver = Driver()

        basic_time_step = int(self.driver.getBasicTimeStep())
        sensor_time_step = 4 * basic_time_step

        # Lidar
        self.lidar = Lidar("RpLidarA2")
        self.lidar.enable(sensor_time_step)
        self.lidar.enablePointCloud()

        # Camera
        self.camera = Camera("realsense_camera")
        self.camera.enable(sensor_time_step)

        # Lidar
        self.depth = RangeFinder("realsense_depth")
        self.depth.enable(sensor_time_step)

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            lidar = session.declare_publisher("marcsrover/lidar")
            camera = session.declare_publisher("marcsrover/opencv-camera")

            try:
                while self.driver.step() != -1:
                    lidar_data = self.lidar.getRangeImage()
                    lidar_data = [i * 1000 for i in lidar_data]

                    bytes = LidarScan(
                        qualities=[],
                        angles=[i for i in range(360)],
                        distances=lidar_data,
                    ).serialize()

                    lidar.put(bytes)

                    camera_data = self.camera.getImage()
                    image = np.frombuffer(camera_data, dtype=np.uint8).reshape(
                        (240, 320, 4)
                    )
                    # remove the 4th channel
                    image = image[:, :, 0:3]

                    jpg_frame = cv2.imencode(
                        ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 50]
                    )[1].tobytes()

                    bytes = OpenCVCamera(jpg_frame).serialize()

                    camera.put(bytes)

            except KeyboardInterrupt:
                print("Received KeyboardInterrupt")

            camera.undeclare()
            lidar.undeclare()
            session.close()

        print("Node stopped")


def launch_node():
    node = Node()
    node.run()


launch_node()
