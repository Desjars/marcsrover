import signal
import time
import threading

import zenoh
import cv2

import numpy as np
import dearpygui.dearpygui as dpg

from message import D435I, JoyStickController, LidarScan

class Monitoring:
    def __init__(self):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.ctrl_c_signal)
        signal.signal(signal.SIGTERM, self.ctrl_c_signal)

        self.running = True
        self.mutex = threading.Lock()

        # Create node variables

        self.width = 1280
        self.height = 960

        dpg.create_context()
        dpg.create_viewport(title='MARCSRover', width=self.width, height=self.height)
        dpg.setup_dearpygui()

        with dpg.texture_registry():
            dpg.add_raw_texture(640, 480, [], tag="realsense_color", format=dpg.mvFormat_Float_rgb)
            dpg.add_raw_texture(640, 480, [], tag="realsense_depth", format=dpg.mvFormat_Float_rgb)

        with dpg.window(label="Realsense", width=1280, height=480, pos=(0, 0)):
            dpg.add_image("realsense_color", pos=(0, 0))
            dpg.add_image("realsense_depth", pos=(640, 0))

        with dpg.window(tag="LiDAR", width=640, height=480, pos=(0, 480)):
            pass

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/subs
        self.stop_handler = self.session.declare_publisher("marcsrover/stop")
        self.lidar_sub = self.session.declare_subscriber("marcsrover/lidar", self.lidar_callback)
        self.realsense_sub = self.session.declare_subscriber("marcsrover/realsense", self.realsense_callback)
        self.controller_sub = self.session.declare_subscriber("marcsrover/controller", self.controller_callback)

    def run(self):
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

            # Check if the node should stop

            self.mutex.acquire()
            running = self.running
            self.mutex.release()

            if not running:
                break

        self.close()

    def close(self):
        # self.stop_handler.put([])
        self.stop_handler.undeclare()
        self.lidar_sub.undeclare()
        self.realsense_sub.undeclare()
        self.session.close()

        dpg.destroy_context()

    def lidar_callback(self, sample):
        lidar = LidarScan.deserialize(sample.value.payload)

    def realsense_callback(self, sample):
        image = D435I.deserialize(sample.value.payload)
        rgb = np.frombuffer(bytes(image.rgb), dtype=np.uint8)
        rgb = cv2.imdecode(rgb, cv2.IMREAD_COLOR)
        depth = np.frombuffer(bytes(image.depth), dtype=np.uint8)
        depth = cv2.imdecode(depth, cv2.IMREAD_COLOR)

        data = np.flip(rgb, 2)
        data = data.ravel()
        data = np.asarray(data, dtype='f')

        texture_data = np.true_divide(data, 255.0)
        dpg.set_value("realsense_color", texture_data)

        data = np.flip(depth, 2)
        data = data.ravel()
        data = np.asarray(data, dtype='f')

        texture_data = np.true_divide(data, 255.0)
        dpg.set_value("realsense_depth", texture_data)

    def controller_callback(self, sample):
        controller = JoyStickController.deserialize(sample.value.payload)

    def ctrl_c_signal(self, signum, frame):
        # Stop the node

        self.mutex.acquire()
        self.running = False
        self.mutex.release()

        # Put your cleanup code here

if __name__ == "__main__":
    monitoring = Monitoring()
    monitoring.run()
