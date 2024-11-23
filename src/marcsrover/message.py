from dataclasses import dataclass

from pycdr2 import IdlStruct
from pycdr2.types import float32, uint8


@dataclass
class JoyStickMotor(IdlStruct):
    speed: float32
    steering: float32
    gear: uint8
