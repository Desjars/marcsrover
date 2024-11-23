from dataclasses import dataclass

from pycdr2 import IdlStruct
from pycdr2.types import int32, float32, uint32
from typing import List

@dataclass
class D435I(IdlStruct):
    rgb: bytes
    depth: bytes
    width: uint32
    height: uint32
    depth_factor: float32

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
