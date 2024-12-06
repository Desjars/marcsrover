import zenoh
import json
import threading

import numpy as np
import cv2

from vehicle import Driver
from controller import Lidar, Camera, RangeFinder, Accelerometer, Gyro

from dataclasses import dataclass

from pycdr2 import IdlStruct
from pycdr2.types import float32, int32
from typing import List


@dataclass
class OpenCVCamera(IdlStruct):
    frame: bytes


@dataclass
class LidarScan(IdlStruct):
    qualities: List[float32]
    angles: List[float32]
    distances: List[float32]


@dataclass
class RoverControl(IdlStruct):
    speed: int32
    steering: int32

@dataclass
class IMU(IdlStruct):
    accel_x: float32
    accel_y: float32
    accel_z: float32
    gyro_x: float32
    gyro_y: float32
    gyro_z: float32


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

        # Accelerometer
        self.accel = Accelerometer("accelerometer")
        self.accel.enable(sensor_time_step)

        # Gyro
        self.gyro = Gyro("gyro")
        self.gyro.enable(sensor_time_step)

        self.mutex = threading.Lock()
        self.speed = 0
        self.steer = 0

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            lidar = session.declare_publisher("marcsrover/lidar")
            camera = session.declare_publisher("marcsrover/opencv-camera")

            control = session.declare_subscriber(
                "marcsrover/control", self.control_callback
            )

            imu = session.declare_publisher("marcsrover/imu")

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

                    accel = self.accel.getValues()
                    gyro = self.gyro.getValues()

                    bytes = IMU(
                        accel_x=accel[0],
                        accel_y=accel[1],
                        accel_z=accel[2],
                        gyro_x=gyro[0],
                        gyro_y=gyro[1],
                        gyro_z=gyro[2],
                    ).serialize()

                    imu.put(bytes)

                    self.mutex.acquire()
                    self.driver.setSteeringAngle(self.steer)
                    self.driver.setCruisingSpeed(self.speed)

                    self.mutex.release()

            except KeyboardInterrupt:
                print("Received KeyboardInterrupt")

            camera.undeclare()
            lidar.undeclare()
            imu.undeclare()
            control.undeclare()
            session.close()

        print("Node stopped")

    def control_callback(self, sample: zenoh.Sample) -> None:
        motor = RoverControl.deserialize(sample.payload.to_bytes())

        self.mutex.acquire()

        self.speed = motor.speed / 1000
        self.steer = ((motor.steering + 90) * (16 - (-16)) / 180 + (-16)) * np.pi / 180

        self.mutex.release()


def launch_node():
    node = Node()
    node.run()


launch_node()
