import zenoh
import threading
import json
import cv2

import pyrealsense2 as rs
import numpy as np

from marcsrover.message import D435I
from typing import Tuple


class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7446"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/127.0.0.1:0"])
        )

        self.pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

    def get_frame(self) -> Tuple[bool, cv2.UMat | None, cv2.UMat | None]:
        try:
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            if not depth_frame or not color_frame:
                return False, None, None

            return True, depth_image, color_image
        except:
            return False, None, None

    def run(self, stop_event: threading.Event) -> None:
        with zenoh.open(self.zenoh_config) as session:
            realsense = session.declare_publisher("marcsrover/realsense")

            while not stop_event.is_set():
                ret, depth_frame, color_frame = self.get_frame()

                if not ret:
                    continue

                if color_frame is None or depth_frame is None:
                    continue

                color_frame = cv2.imencode(
                    ".jpg", color_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50]
                )[1].tobytes()

                min, max, _, _ = cv2.minMaxLoc(depth_frame)
                cv2.normalize(
                    depth_frame, depth_frame, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1
                )
                depth_frame = cv2.imencode(
                    ".jpg", depth_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50]
                )[1].tobytes()

                bytes = D435I(
                    rgb=color_frame,
                    depth=depth_frame,
                    width=640,
                    height=480,
                    depth_factor=max / 255.0,
                ).serialize()

                realsense.put(bytes)

            realsense.undeclare()
            session.close()
            self.pipeline.stop()

        print("Realsense node stopped")


def launch_node(stop_event: threading.Event) -> None:
    node = Node()

    node.run(stop_event)
