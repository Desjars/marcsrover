import argparse
import os

import cv2
import numpy as np
import pyarrow as pa

import zenoh

from dora import Node

def main():

    # Handle dynamic nodes, ask for the name of the node in the dataflow, and the same values as the ENV variables.
    parser = argparse.ArgumentParser(
        description="Zenoh Publish: This node is used to bridge data between two zenoh instances."
    )

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="zenoh-publish",
    )

    args = parser.parse_args()

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    config = zenoh.Config.from_file("../zenoh_config.json")
    session = zenoh.open(config)

    image_publisher = session.declare_publisher("marcsrover/image")

    pa.array([])  # initialize pyarrow array

    for event in node:
        event_type = event["type"]

        if event_type == "INPUT":
            event_id = event["id"]

            if event_id == "image":
                storage = event["value"]

                metadata = event["metadata"]
                width = metadata["width"]
                height = metadata["height"]

                channels = 3
                frame = (
                    storage.to_numpy()
                    .reshape((height, width, channels))
                )

                frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])[1]
                image_publisher.put(frame.tobytes())

        elif event_type == "ERROR":
            raise RuntimeError(event["error"])


if __name__ == "__main__":
    main()
