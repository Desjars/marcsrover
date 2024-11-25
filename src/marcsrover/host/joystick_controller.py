import zenoh
import json
import pygame

import numpy as np

from pygame.constants import (
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYBUTTONDOWN,
    JOYBUTTONUP,
    JOYHATMOTION,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
)

from marcsrover.message import RoverControl


class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7447"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/127.0.0.1:0"])
        )
        self.zenoh_config.insert_json5("scouting/gossip/enabled", json.dumps(True))

        pygame.init()
        pygame.event.set_blocked((MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN))

        self.gear = 5

        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

        self.axis = []
        for i in range(self.joy.get_numaxes()):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.joy.get_numballs()):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.joy.get_numbuttons()):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.joy.get_numhats()):
            self.hat.append(self.joy.get_hat(i))

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
                        elif event.type == JOYAXISMOTION:
                            self.axis[event.axis] = event.value
                        elif event.type == JOYBALLMOTION:
                            self.ball[event.ball] = event.rel
                        elif event.type == JOYHATMOTION:
                            self.hat[event.hat] = event.value
                        elif event.type == JOYBUTTONUP:
                            self.button[event.button] = 0
                        elif event.type == JOYBUTTONDOWN:
                            self.button[event.button] = 1

                    steering_x = self.axis[1]
                    steering_y = self.axis[0]

                    steering = int(np.arctan2(steering_y, 1 - steering_x) * 180 / np.pi)

                    dec = self.button[6]
                    inc = self.button[7]

                    if dec and self.gear >= 2:
                        self.gear -= 1
                    if inc and self.gear <= 9:
                        self.gear += 1

                    speed = int(-self.axis[3] * (self.gear * 200))

                    bytes = RoverControl(speed, steering).serialize()

                    rover_control.put(bytes)
            except KeyboardInterrupt:
                print("Joystick node received KeyboardInterrupt")

            rover_control.undeclare()

            session.close()

        print("Joystick node stopped")


node = Node()
node.run()
