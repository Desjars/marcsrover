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
        description="Zenoh Receive: This node is used to bridge data between two zenoh instances."
    )

    parser.add_argument(
        "--name",
        type=str,
        required=False,
        help="The name of the node in the dataflow.",
        default="zenoh-receive",
    )

    args = parser.parse_args()

    node = Node(
        args.name
    )  # provide the name to connect to the dataflow if dynamic node

    config = zenoh.Config.from_file("../zenoh_config.json")
    session = zenoh.open(config)

    pa.array([])  # initialize pyarrow array

    def image_callback(sample):
        node.send_output("image", pa.array([]))

    image_subscriber = session.declare_subscriber("marcsrover/image", image_callback)

    import time

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
