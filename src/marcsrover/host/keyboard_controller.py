import zenoh
import json

from marcsrover.message import RoverControl

from pynput import keyboard


class Node:
    def __init__(self):
        zenoh.init_log_from_env_or("info")

        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7447"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/0.0.0.0:0"])
        )
        self.zenoh_config.insert_json5("scouting/multicast/enabled", json.dumps(False))
        self.zenoh_config.insert_json5("scouting/gossip/enabled", json.dumps(True))

        self.keys = {
            keyboard.Key.up: False,
            keyboard.Key.down: False,
            keyboard.Key.left: False,
            keyboard.Key.right: False,
        }

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            rover_control = session.declare_publisher("marcsrover/control")

            try:
                with keyboard.Events() as events:
                    for event in events:
                        str_event = f"{event}"
                        type = str_event.split("(")[0]

                        speed = 0
                        steering = 0

                        if type == "Press":
                            self.keys[event.key] = True
                        elif type == "Release":
                            self.keys[event.key] = False

                        if self.keys[keyboard.Key.up]:
                            speed = 3000
                        elif self.keys[keyboard.Key.down]:
                            speed = -3000

                        if self.keys[keyboard.Key.left]:
                            steering = -90
                        elif self.keys[keyboard.Key.right]:
                            steering = 90

                        bytes = RoverControl(speed, steering).serialize()
                        rover_control.put(bytes)

            except KeyboardInterrupt:
                print("Keyboard control node stopped")

            rover_control.undeclare()
            session.close()


def launch_node():
    node = Node()
    node.run()
