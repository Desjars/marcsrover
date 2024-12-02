import zenoh
import json
import time

from pyrplidar import PyRPlidar

from marcsrover.message import LidarScan


class Node:
    def __init__(self, lidar_port):
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

        self.lidar = PyRPlidar()
        self.lidar.connect(lidar_port, 256000, 3)

        # The LiDAR may not have been stopped properly, so we need to reset it

        self.lidar.set_motor_pwm(0)
        self.lidar.stop()
        self.lidar.disconnect()

        time.sleep(2)  # Wait for the lidar to stop

        # Now we can start

        self.lidar.connect(lidar_port, 256000, 3)
        self.lidar.set_motor_pwm(500)

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            time.sleep(2)  # Wait for the lidar to start
            scan_generator = self.lidar.start_scan()

            qualities = []
            angles = []
            distances = []

            lidar_publisher = session.declare_publisher("marcsrover/lidar")

            start_tag = False

            try:
                for count, scan in enumerate(scan_generator()):
                    quality = scan.quality
                    angle = scan.angle
                    distance = scan.distance

                    if not start_tag:
                        if angle < 1.0:
                            start_tag = True

                        continue

                    if (
                        angle > 2 and angle < 355
                    ):  # dead zone but it's necessary to have a full scan
                        qualities.append(quality)
                        angles.append(angle)
                        distances.append(distance)
                    else:
                        if len(angles) > 300:
                            bytes = LidarScan(
                                qualities=qualities, angles=angles, distances=distances
                            ).serialize()
                            lidar_publisher.put(bytes)

                        qualities = []
                        angles = []
                        distances = []

            except KeyboardInterrupt:
                print("LiDAR Received KeyboardInterrupt")

            lidar_publisher.undeclare()

            session.close()

            self.lidar.set_motor_pwm(0)
            self.lidar.disconnect()

        print("LiDAR node stopped")


def launch_node(args):
    node = Node(args.lidar_port)
    node.run()
