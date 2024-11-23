import zenoh
import threading
import json
import time

from pyrplidar import PyRPlidar

from marcsrover.message import LidarScan


class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7447"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/127.0.0.1:0"])
        )

        self.lidar = PyRPlidar()
        self.lidar.connect("/dev/ttyUSB0", 256000, 3)

        # The LiDAR may not have been stopped properly, so we need to reset it

        self.lidar.set_motor_pwm(0)
        self.lidar.stop()
        self.lidar.disconnect()

        time.sleep(2)  # Wait for the lidar to stop

        # Now we can start

        self.lidar.connect("/dev/ttyUSB0", 256000, 3)
        self.lidar.set_motor_pwm(500)

    def run(self, stop_event: threading.Event) -> None:
        with zenoh.open(self.zenoh_config) as session:
            time.sleep(2)  # Wait for the lidar to start
            scan_generator = self.lidar.start_scan()

            qualities = []
            angles = []
            distances = []

            lidar_publisher = session.declare_publisher("marcsrover/lidar")

            for count, scan in enumerate(scan_generator()):
                if stop_event.is_set():
                    break

                quality = scan.quality
                angle = scan.angle
                distance = scan.distance

                if angle < 1:  # When the angle is less than 1, we have a full tour scan
                    bytes = LidarScan(
                        qualities=qualities, angles=angles, distances=distances
                    ).serialize()
                    lidar_publisher.put(bytes)

                    qualities = []
                    angles = []
                    distances = []

                qualities.append(quality)
                angles.append(angle)
                distances.append(distance)

            lidar_publisher.undeclare()

            session.close()

        print("LiDAR node stopped")


def launch_node(stop_event: threading.Event) -> None:
    node = Node()

    node.run(stop_event)
