from pygame.constants import KEYDOWN, KEYUP
import zenoh
import json
import pygame
from marcsrover.message import RoverControl


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

        pygame.init()
        pygame.display.set_mode((300, 300))

        pygame.event.set_blocked(
            (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN)
        )

        self.keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
        }

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            rover_control = session.declare_publisher("marcsrover/control")

            try:
                while True:
                    events = pygame.event.get()

                    num_events = len(events)
                    if num_events == 0:
                        continue

                    for event in events:
                        if event.type == pygame.QUIT:
                            break
                        elif event.type == KEYDOWN:
                            if event.key in self.keys:
                                self.keys[event.key] = True
                        elif event.type == KEYUP:
                            if event.key in self.keys:
                                self.keys[event.key] = False

                    speed = 0
                    steering = 0

                    if self.keys[pygame.K_UP]:
                        speed = 3000
                    elif self.keys[pygame.K_DOWN]:
                        speed = -3000

                    if self.keys[pygame.K_LEFT]:
                        steering = -45
                    elif self.keys[pygame.K_RIGHT]:
                        steering = 45

                    bytes = RoverControl(speed, steering).serialize()
                    rover_control.put(bytes)

            except KeyboardInterrupt:
                print("Keyboard control node stopped")

            rover_control.undeclare()
            session.close()
            pygame.quit()


def launch_node():
    node = Node()
    node.run()
