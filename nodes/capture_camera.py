import argparse
import os
import time

import cv2
import numpy as np
import pyarrow as pa

import zenoh

def main():
    video_capture_path = "/dev/video0"

    if isinstance(video_capture_path, str) and video_capture_path.isnumeric():
        video_capture_path = int(video_capture_path)

    video_capture = cv2.VideoCapture(video_capture_path)

    image_width = 640
    image_height = 480

    pa.array([])  # initialize pyarrow array

    config = zenoh.Config.from_file("zenoh_config.json")
    session = zenoh.open(config)

    camera_publisher = session.declare_publisher("marcsrover/camera")

    while True:
        ret, frame = video_capture.read()

        if not ret:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(
                frame,
                f"Error: no frame for camera at path {video_capture_path}.",
                (int(30), int(30)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (255, 255, 255),
                1,
                1,
            )

        frame = cv2.resize(frame, (image_width, image_height))
        frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])[1].tobytes()

        camera_publisher.put(frame)

if __name__ == "__main__":
    main()
