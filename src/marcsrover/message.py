from dataclasses import dataclass

from pycdr2 import IdlStruct
from pycdr2.types import int32, float32
from typing import List


@dataclass
class OpenCVCamera(IdlStruct):
    frame: bytes


@dataclass
class RoverControl(IdlStruct):
    speed: int32
    steering: int32


@dataclass
class LidarScan(IdlStruct):
    qualities: List[float32]
    angles: List[float32]
    distances: List[float32]
