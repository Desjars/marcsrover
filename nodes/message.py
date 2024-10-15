from dataclasses import dataclass

import numpy as np
import json

from pycdr2 import IdlStruct
from pycdr2.types import uint32, float32
from typing import List

@dataclass
class CameraFrame(IdlStruct):
    frame: bytes
    width: uint32
    height: uint32

@dataclass
class JoyStick(IdlStruct):
    axes: List[float32]
    buttons: List[uint32]
    balls: List[float32]

@dataclass
class LidarScan(IdlStruct):
    qualities: List[float32]
    angles: List[float32]
    distances: List[float32]
