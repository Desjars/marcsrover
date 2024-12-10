import zenoh
import json
import threading

import numpy as np

from marcsrover.message import AutoPilotConfig, LidarScan, RoverControl


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

        self.min_speed = 0
        self.max_speed = 0
        self.back_speed = 0
        self.steering = 90
        self.back_treshold = 0.5
        self.fwd_treshold = 0.5
        self.steering_treshold = 0.5
        self.steering_min_angle = 45
        self.steering_max_angle = 90

        self.mutex = threading.Lock()

    def callback(self, sample: zenoh.Sample):
        with self.mutex:
            config = AutoPilotConfig.deserialize(sample.payload.to_bytes())

            self.min_speed = config.min_speed
            self.max_speed = config.max_speed
            self.back_speed = config.back_speed
            self.steering = config.steering
            self.back_treshold = config.back_treshold
            self.fwd_treshold = config.fwd_treshold
            self.steering_treshold = config.steering_treshold
            self.steering_min_angle = config.steering_min_angle
            self.steering_max_angle = config.steering_max_angle

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            self.rover_control = session.declare_publisher("marcsrover/control")

            self.config = session.declare_subscriber(
                "marcsrover/autopilot/config", self.callback
            )

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

        with self.mutex:
            lidar = LidarScan.deserialize(sample.payload.to_bytes())

            # speed control : On fait une moyenne des espaces angles entre 350 et 10 degrés, cela donne la vitesse à laquelle on doit avancer
            angles = np.array(lidar.angles)
            indices = np.where((angles >= 350) | (angles <= 10))
            distances = np.array(lidar.distances)[indices]
            mean = np.mean(distances) / 1000

            speed = 0

            if mean < self.back_treshold:
                speed = -self.back_speed
            elif mean < self.fwd_treshold:
                speed = self.min_speed
            else:
                speed = self.max_speed

            # steering control : On fait deux moyenne, l'une entre 45 et 90 degrés, l'autre entre 270 et 315 degrés. On fait la différence
            # entre les deux moyennes, cela donne la direction dans laquelle on doit tourner. Si la différence est négative, on tourne à
            # gauche, si elle est positive on tourne à droite.
            indices1 = np.where(
                (angles >= self.steering_min_angle)
                & (angles <= self.steering_max_angle)
            )
            indices2 = np.where(
                (angles >= 360 - self.steering_max_angle)
                & (angles <= 360 - self.steering_min_angle)
            )

            distances1 = np.array(lidar.distances)[indices1]
            distances2 = np.array(lidar.distances)[indices2]

            mean1 = np.mean(distances1) / 1000
            mean2 = np.mean(distances2) / 1000

            steering = 0

            if mean1 - mean2 < -self.steering_treshold:
                steering = -self.steering
            elif mean1 - mean2 > self.steering_treshold:
                steering = self.steering

            if mean < self.back_treshold:
                steering = -steering

            speed = min(1000, speed)

            bytes = RoverControl(speed, steering).serialize()

            self.rover_control.put(bytes)


def launch_node():
    node = Node()
    node.run()
