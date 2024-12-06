import zenoh
import json

import numpy as np

from marcsrover.message import LidarScan, RoverControl


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

        self.rover_control = None

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            self.rover_control = session.declare_publisher("marcsrover/control")

            lidar = session.declare_subscriber("marcsrover/lidar", self.lidar_callback)

            try:
                while True:
                    pass

            except KeyboardInterrupt:
                print("Auto Pilot node received KeyboardInterrupt")

            self.rover_control.undeclare()
            lidar.undeclare()
            session.close()

        print("Auto Pilot node stopped")

    def lidar_callback(self, sample: zenoh.Sample) -> None:
        if self.rover_control is None:
            return

        lidar = LidarScan.deserialize(sample.payload.to_bytes())

        # speed control : On fait une moyenne des espaces angles entre 350 et 10 degrés, cela donne la vitesse à laquelle on doit avancer
        angles = np.array(lidar.angles)
        indices = np.where((angles >= 350) | (angles <= 10))
        distances = np.array(lidar.distances)[indices]
        mean = np.mean(distances) / 1000

        speed = 0

        if mean < 0.5:
            speed = -1500
        elif mean < 1:
            speed = 2000
        elif mean < 2:
            speed = 3000
        else:
            speed = 4000

        # steering control : On fait deux moyenne, l'une entre 45 et 90 degrés, l'autre entre 270 et 315 degrés. On fait la différence
        # entre les deux moyennes, cela donne la direction dans laquelle on doit tourner. Si la différence est négative, on tourne à
        # gauche, si elle est positive on tourne à droite. On va dire que si la différence est inférieure à 10 degrés, on ne tourne pas
        # et si elle est supérieure à 30 degrés, on tourne à fond.

        indices1 = np.where((angles >= 45) & (angles <= 90))
        indices2 = np.where((angles >= 270) & (angles <= 315))

        distances1 = np.array(lidar.distances)[indices1]
        distances2 = np.array(lidar.distances)[indices2]

        mean1 = np.mean(distances1) / 1000
        mean2 = np.mean(distances2) / 1000

        steering = 0

        if mean1 - mean2 < -0.5:
            steering = -90
        elif mean1 - mean2 > 0.5:
            steering = 90

        if mean < 0.5:
            steering = -steering

        bytes = RoverControl(speed, steering).serialize()

        self.rover_control.put(bytes)


def launch_node():
    node = Node()
    node.run()
