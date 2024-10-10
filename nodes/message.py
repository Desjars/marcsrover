from dataclasses import dataclass

import numpy as np
import json

from pycdr2 import IdlStruct
from pycdr2.types import uint32
from typing import List

@dataclass
class CameraFrame(IdlStruct):
    frame: bytes
    width: uint32
    height: uint32

"""
example of a LidarScan message
@dataclass
class LidarScan(IdlStruct):
    ranges: List[float]
    intensities: List[float]
    angle_min: float
    angle_max: float
    angle_increment: float
    time_increment: float
    scan_time: float
    range_min: float
    range_max: float
"""

"""
example of a Joystick message
@dataclass
class Joystick(IdlStruct):
    axes: List[float]
    buttons: List[uint32]
"""
