import zenoh
import signal
import json

import threading

from marcsrover.host.joystick_controller import launch_node as launch_joystick_node
from marcsrover.host.monitor import launch_node as launch_monitor_node
from marcsrover.common.opencv_camera import launch_node as launch_camera_node


def signal_handler(sig, frame):
    print("Interrupted")


def run() -> None:
    zenoh.init_log_from_env_or("info")

    router_config: zenoh.Config = zenoh.Config.from_json5("{}")

    router_config.insert_json5("listen/endpoints", json.dumps(["udp/127.0.0.1:7447"]))

    # === HERE, CONNECT TO THE ZENOH ROUTER RUNNING ON THE ROVER ===
    #
    # The following code connects to the Zenoh router running on the rover.
    #
    # router_config.insert_json5("connect/endpoints", json.dumps([
    #     "udp/...:7447"
    # ]))

    with zenoh.open(router_config) as session:
        signal.signal(signal.SIGINT, signal_handler)

        # === Launch all nodes ===
        #
        # The following code launches all the nodes in the system.

        stop_event = threading.Event()

        joystick = threading.Thread(target=launch_joystick_node, args=(stop_event,))
        joystick.start()

        monitor = threading.Thread(target=launch_monitor_node, args=(stop_event,))
        monitor.start()

        opencv_camera = threading.Thread(target=launch_camera_node, args=(stop_event,))
        opencv_camera.start()

        print("Press Ctrl+C to quit")
        signal.pause()

        # === End nodes ===
        #
        # Interrupt all the nodes in the system.

        stop_event.set()

        opencv_camera.join()
        joystick.join()
        monitor.join()

        session.close()
