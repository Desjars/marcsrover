import zenoh
import threading
import json

import cv2

import numpy as np

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

        self.video_capture = cv2.VideoCapture("/dev/video0")
        self.width = 640
        self.height = 480

    def run(self, stop_event: threading.Event) -> None:
        with zenoh.open(self.zenoh_config) as session:
            camera = session.declare_publisher("marcsrover/opencv-camera")

            while not stop_event.is_set():
                (ret, frame) = self.video_capture.read()

                if not ret:
                    frame = np.zeros((self.width, self.height, 3), dtype=np.uint8)
                    cv2.putText(
                        frame,
                        "Error: no frame for this camera.",
                        (int(30), int(30)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.50,
                        (255, 255, 255),
                        1,
                        1,
                    )

                frame = cv2.resize(frame, (self.width, self.height))
                jpg_frame = cv2.imencode(
                    ".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50]
                )[1].tobytes()

                bytes = OpenCVCamera(jpg_frame).serialize()

                camera.put(bytes)

            camera.undeclare()
            session.close()

        print("OpenCV Camera node stopped")


def launch_node(stop_event: threading.Event) -> None:
    node = Node()

    node.run(stop_event)
