import zenoh
import json
import pygame
import numpy as np
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
        pygame.display.set_mode((400, 300))  # Crée une fenêtre pour que Pygame fonctionne
        pygame.event.set_blocked((pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN))

        self.gear = 5  # Vitesse initiale
        self.steering = 0  # Angle initial de direction
        self.speed = 0  # Vitesse initiale

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            rover_control = session.declare_publisher("marcsrover/control")
            try:
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            raise KeyboardInterrupt

                    # Récupérer l'état des touches
                    keys = pygame.key.get_pressed()

                    # Contrôle de la direction (flèches gauche et droite)
                    if keys[pygame.K_LEFT]:
                        self.steering = max(self.steering - 5, -45)  # Limite à -45 degrés
                    elif keys[pygame.K_RIGHT]:
                        self.steering = min(self.steering + 5, 45)  # Limite à 45 degrés
                    else:
                        self.steering = 0  # Retour au centre

                    # Contrôle de la vitesse (flèches haut et bas)
                    if keys[pygame.K_UP]:
                        self.speed = min(self.speed + self.gear * 20, 1000)  # Limite supérieure
                    elif keys[pygame.K_DOWN]:
                        self.speed = max(self.speed - self.gear * 20, -1000)  # Limite inférieure
                    else:
                        self.speed = 0  # Arrêt progressif

                    # Changer la vitesse maximale (gear) avec touches +/- ou autres
                    if keys[pygame.K_MINUS] and self.gear > 1:
                        self.gear -= 1
                    if keys[pygame.K_PLUS] and self.gear < 9:
                        self.gear += 1

                    # Envoyer les commandes au rover
                    bytes = RoverControl(self.speed, self.steering).serialize()
                    rover_control.put(bytes)

            except KeyboardInterrupt:
                print("Keyboard control node stopped")

            rover_control.undeclare()
            session.close()


def launch_node():
    node = Node()
    node.run()