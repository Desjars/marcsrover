import zenoh
import json
import time

import dearpygui.dearpygui as dpg

from marcsrover.host.monitor.IMU import init_imu
from marcsrover.host.monitor.controller import init_controller
from marcsrover.host.monitor.main_window import init_main_window
from marcsrover.host.monitor.auto_pilot import init_autopilot


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

        dpg.create_context()
        dpg.create_viewport(
            title="MARCSRover",
            width=1280,
            height=720,
            x_pos=1920 // 2 - 1280 // 2,
            y_pos=1280 // 2 - 720 // 2,
        )
        dpg.setup_dearpygui()

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            init_controller(session)
            init_main_window(session)
            init_imu(session)
            init_autopilot(session)

            dpg.show_viewport()
            try:
                while dpg.is_dearpygui_running():
                    dpg.render_dearpygui_frame()
                    time.sleep(1 / 30)
            except KeyboardInterrupt:
                print("Monitor received KeyboardInterrupt")

            dpg.destroy_context()
            session.close()

        print("Monitor stopped")


def launch_node():
    node = Node()
    node.run()
