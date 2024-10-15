import signal
import time
import threading

import zenoh

import pyrealsense2 as rs
import numpy as np

from message import D435I

class Realsense:
    def __init__(self):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.ctrl_c_signal)
        signal.signal(signal.SIGTERM, self.ctrl_c_signal)

        self.running = True
        self.mutex = threading.Lock()

        # Create node variables
        self.pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)


        # Start streaming
        self.pipeline.start(config)

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/sub
        self.stop_handler = self.session.declare_subscriber("marcsrover/stop", self.zenoh_stop_signal)
        self.realsense_publisher = self.session.declare_publisher("marcsrover/realsense")

    def run(self):
        while True:
            # Check if the node should stop

            self.mutex.acquire()
            running = self.running
            self.mutex.release()

            if not running:
                break

            ret, depth_frame, color_frame = self.get_frame()
            if not ret:
                continue

            image = D435I(
                rgb=color_frame.ravel(),
                depth=depth_frame.ravel(),
                width=640,
                height=480
                )

            self.realsense_publisher.put(D435I.serialize(image))

        self.close()

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        if not depth_frame or not color_frame:
            return False, None, None

        return True, depth_image, color_image


    def close(self):
        self.stop_handler.undeclare()
        self.realsense_publisher.undeclare()
        self.session.close()

        self.pipeline.stop()

    def ctrl_c_signal(self, signum, frame):
        # Stop the node

        self.mutex.acquire()
        self.running = False
        self.mutex.release()

        # Put your cleanup code here

    def zenoh_stop_signal(self, sample):
        # Stop the node

        self.mutex.acquire()
        self.running = False
        self.mutex.release()

if __name__ == "__main__":
    node = Realsense()
    node.run()
