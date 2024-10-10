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
