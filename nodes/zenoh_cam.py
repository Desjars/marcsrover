import argparse
import os

import cv2
import numpy as np
import pyarrow as pa

import zenoh

from dora import Node

def main():
    node = Node(
        "zenoh-camera"
    )  # provide the name to connect to the dataflow if dynamic node

    config = zenoh.Config.from_file("../config.json")
    session = zenoh.open(config)

    pa.array([])  # initialize pyarrow array

    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":
            event_id = event["id"]

            if event_id == "image":
                image = event["value"].to_numpy()
                image = image.reshape((480, 640, 3))
                (_, jpeg) = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 15])
                session.put("marcsrover/image", jpeg.tobytes())

                print("image sent", flush=True)


        elif event_type == "ERROR":
            raise RuntimeError(event["error"])


if __name__ == "__main__":
    main()
