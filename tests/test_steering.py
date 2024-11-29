import numpy as np
import time

from marcsrover.car.servo import DynamixelBus, TorqueMode

bus = DynamixelBus("/dev/ttyUSB0", {"steering": (1, "xl430-w250")})

bus.write_torque_enable(TorqueMode.ENABLED, "steering")
for _ in range(3):
    bus.write_goal_position(np.uint32(2048), "steering")
    time.sleep(0.3)
    bus.write_goal_position(np.uint32(1630), "steering")
    time.sleep(0.3)

bus.write_goal_position(np.uint32(2048 + 1630) // 2, "steering")
time.sleep(0.3)

bus.write_torque_enable(TorqueMode.DISABLED, "steering")
bus.close()
