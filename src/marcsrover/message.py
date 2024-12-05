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
