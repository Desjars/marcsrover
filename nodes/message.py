from dataclasses import dataclass

import numpy as np
import json

from pycdr2 import IdlStruct
from pycdr2.types import uint32, float32, uint8
from typing import List

@dataclass
class D435I(IdlStruct):
    rgb: bytes
    depth: bytes
    width: uint32
    height: uint32
    depth_factor: float32

@dataclass
class JoyStickController(IdlStruct):
    axis: List[float32]
    buttons: List[uint32]
    balls: List[float32]

@dataclass
class Motor(IdlStruct):
    speed: float32
    steering: float32
    gear: uint8

@dataclass
class LidarScan(IdlStruct):
    qualities: List[float32]
    angles: List[float32]
    distances: List[float32]
