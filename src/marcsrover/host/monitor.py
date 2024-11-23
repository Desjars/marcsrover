import zenoh
import threading
import json
import cv2

import numpy as np
import dearpygui.dearpygui as dpg

from marcsrover.message import OpenCVCamera


class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7447"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/127.0.0.1:0"])
        )

        dpg.create_context()
        dpg.create_viewport(
            title="MARCSRover",
            width=1280,
            height=960,
            x_pos=1920 // 2 - 1280 // 2,
            y_pos=1280 // 2 - 960 // 2,
        )
        dpg.setup_dearpygui()

    def run(self, stop_event: threading.Event) -> None:
        with zenoh.open(self.zenoh_config) as session:
            camera = session.declare_subscriber(
                "marcsrover/opencv-camera", self.opencv_camera_callback
            )

            dpg.show_viewport()

            with dpg.texture_registry():
                dpg.add_raw_texture(
                    640, 480, [], tag="opencv-camera", format=dpg.mvFormat_Float_rgb
                )

            with dpg.window(label="OpenCV Camera", width=1280, height=480, pos=(0, 0)):
                dpg.add_image("opencv-camera", pos=(0, 0))

            while not stop_event.is_set() and dpg.is_dearpygui_running():
                dpg.render_dearpygui_frame()

            dpg.destroy_context()

            camera.undeclare()
            session.close()

        print("Monitor node stopped")

    def opencv_camera_callback(self, sample: zenoh.Sample) -> None:
        image: OpenCVCamera = OpenCVCamera.deserialize(sample.payload.to_bytes())
        rgb = np.frombuffer(bytes(image.frame), dtype=np.uint8)
        rgb = cv2.imdecode(rgb, cv2.IMREAD_COLOR)

        data = np.flip(rgb, 2)
        data = data.ravel()
        data = np.asarray(data, dtype="f")

        texture_data = np.true_divide(data, 255.0)
        try:
            dpg.set_value("opencv-camera", texture_data)
        except:
            print("ERROR")


def launch_node(stop_event: threading.Event) -> None:
    node = Node()

    node.run(stop_event)
