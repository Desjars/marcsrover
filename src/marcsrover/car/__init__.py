import zenoh
import signal
import json

import threading

from marcsrover.car.rover import launch_node as launch_rover_node
from marcsrover.car.lidar import launch_node as launch_lidar_node


def signal_handler(sig, frame):
    print("Interrupted")


def run() -> None:
    zenoh.init_log_from_env_or("info")

    router_config: zenoh.Config = zenoh.Config.from_json5("{}")

    router_config.insert_json5("listen/endpoints", json.dumps(["udp/127.0.0.1:7447"]))

    with zenoh.open(router_config) as session:
        signal.signal(signal.SIGINT, signal_handler)

        # === Launch all nodes ===
        #
        # The following code launches all the nodes in the system.

        stop_event = threading.Event()

        rover = threading.Thread(target=launch_rover_node, args=(stop_event,))
        rover.start()

        lidar = threading.Thread(target=launch_lidar_node, args=(stop_event,))
        lidar.start()

        print("Press Ctrl+C to quit")
        signal.pause()

        # === End nodes ===
        #
        # Interrupt all the nodes in the system.

        stop_event.set()

        lidar.join()
        rover.join()

        session.close()
