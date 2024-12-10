from dataclasses import dataclass

from pycdr2 import IdlStruct
from pycdr2.types import int32, float32
from typing import List


@dataclass
class D435I(IdlStruct):
    rgb: bytes
    depth: bytes


@dataclass
class IMU(IdlStruct):
    accel_x: float32
    accel_y: float32
    accel_z: float32
    gyro_x: float32
    gyro_y: float32
    gyro_z: float32


@dataclass
class BytesMessage(IdlStruct):
    data: bytes


@dataclass
class RoverControl(IdlStruct):
    speed: int32
    steering: int32


@dataclass
class SLAM(IdlStruct):
    x: int32
    y: int32

    cloud_points: bytes  # This is a B&W image 1024x780


@dataclass
class LidarScan(IdlStruct):
    qualities: List[float32]
    angles: List[float32]
    distances: List[float32]


@dataclass
class AutoPilotConfig(IdlStruct):
    min_speed: int32  # 500 - 2000: 1000
    max_speed: int32  # 500 - 2000: 1400
    back_speed: int32  # # 500 - 2000: 1500
    steering: int32  # -100 - 100: 90

    back_treshold: float32  # 0 - 1: 0.5
    fwd_treshold: float32  # 0 - 1: 0.5

    steering_treshold: float32  # 0 - 1: 0.5

    steering_min_angle: int32  # 0 - 90: 45
    steering_max_angle: int32  # 0 - 90: 90

    enable: bool  # True or False: True
