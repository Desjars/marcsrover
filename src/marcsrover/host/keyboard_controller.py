import zenoh
import json
import pygame

import numpy as np


from pygame.locals import (
    QUIT,
    MOUSEMOTION,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    KEYUP,
)

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
        pygame.event.set_blocked((MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN))

        self.gear = 5
        self.speed = 0
        self.steering = 0
        self.keys_pressed = set()

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
                        if event.type == QUIT:
                            break
                        elif event.type == KEYDOWN:
                            self.keys_pressed.add(event.key)
                        elif event.type == KEYUP:
                            self.keys_pressed.discard(event.key)

                    self.update_controls()

                    bytes = RoverControl(self.speed, self.steering).serialize()

                    rover_control.put(bytes)
            except KeyboardInterrupt:
                print("Keyboard control node received KeyboardInterrupt")

            rover_control.undeclare()

            session.close()

        print("Keyboard control node stopped")

    def update_controls(self):
            # Direction : Gauche/Droite
            if pygame.K_LEFT in self.keys_pressed:
                self.steering = max(self.steering - 5, -90)  # Limite : -90° (complètement à gauche)
            elif pygame.K_RIGHT in self.keys_pressed:
                self.steering = min(self.steering + 5, 90)  # Limite : 90° (complètement à droite)
            else:
                self.steering = 0  # Retour au neutre

            # Vitesse : Avant/Arrière
            if pygame.K_UP in self.keys_pressed:
                self.speed = self.gear * 200  # Avancer en fonction de la vitesse
            elif pygame.K_DOWN in self.keys_pressed:
                self.speed = -self.gear * 200  # Reculer en fonction de la vitesse
            else:
                self.speed = 0  # Arrêt

            # Changement de vitesse
            if pygame.K_q in self.keys_pressed and self.gear > 1:  # Décélération (limite à 1)
                self.gear -= 1
                self.keys_pressed.discard(pygame.K_q)  # Pour éviter une répétition rapide
            if pygame.K_e in self.keys_pressed and self.gear < 9:  # Accélération (limite à 9)
                self.gear += 1
                self.keys_pressed.discard(pygame.K_e)  # Pour éviter une répétition rapide



def launch_node():
    node = Node()
    node.run()
