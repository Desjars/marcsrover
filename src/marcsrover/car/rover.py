import zenoh
import json
import serial
import time

import numpy as np

from threading import Lock

from marcsrover.car.servo import DynamixelBus, TorqueMode
from marcsrover.message import RoverControl


class Node:
    def __init__(self, servo_port, microcontroller_port):
        zenoh.init_log_from_env_or("info")

        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7446"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/0.0.0.0:0"])
        )
        self.zenoh_config.insert_json5("scouting/multicast/enabled", json.dumps(False))
        self.zenoh_config.insert_json5("scouting/gossip/enabled", json.dumps(True))

        self.mutex = Lock()

        self.steering = DynamixelBus(
            servo_port, {"steering": (1, "xl430-w250")}
        )

        self.steering.write_torque_enable(TorqueMode.ENABLED, "steering")

        self.speed = serial.Serial(microcontroller_port, 115200, timeout=1)

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            control = session.declare_subscriber(
                "marcsrover/control", self.control_callback
            )

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("Rover Received KeyboardInterrupt")

            control.undeclare()
            session.close()

        print("Rover Node stopped")

    def control_callback(self, sample: zenoh.Sample) -> None:
        motor = RoverControl.deserialize(sample.payload.to_bytes())

        # motor.steering is in range [-90, 90]. Map it to [1630, 2048]
        steering = 1630 + (motor.steering + 90) * (2048 - 1630) / 180
        speed = 4000 + motor.speed

        # at the moment going backward is not really supported, so we will just ignore it and max speed is now 1500
        speed = min(5000, speed)

        self.mutex.acquire()

        self.steering.write_goal_position(np.uint32(steering), "steering")
        self.speed.write((f"s0{speed}" + "\n").encode("utf-8"))

        self.mutex.release()


def launch_node(args):
    node = Node(args.servo_port, args.microcontroller_port)
    node.run()
