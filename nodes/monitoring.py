import signal
import time
import threading

import zenoh
import cv2

import numpy as np
import dearpygui.dearpygui as dpg

from message import D435I, JoyStickController, LidarScan, Motor

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

        with dpg.window(label="LiDAR", tag="LiDAR", width=640, height=480, pos=(0, 480)):
            dpg.add_slider_float(label="LiDAR Scale", tag="LiDAR Scale", width=150, min_value=1, max_value=200, default_value=100)

            with dpg.drawlist(width=640, height=480) as self.lidar_canvas:
                pass

        with dpg.window(label="Controller", width=640, height=480, pos=(640, 480)):
            dpg.add_slider_float(label="Speed", tag="Speed", width=150, min_value=-4000, max_value=4000, default_value=0)
            dpg.add_slider_float(label="Steering", tag="Steering", width=150, min_value=-90, max_value=90, default_value=0)
            dpg.add_slider_int(label="Gear", tag="Gear", width=150, min_value=1, max_value=10, default_value=5)

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/subs
        self.stop_handler = self.session.declare_publisher("marcsrover/stop")
        self.lidar_sub = self.session.declare_subscriber("marcsrover/lidar", self.lidar_callback)
        self.realsense_sub = self.session.declare_subscriber("marcsrover/realsense", self.realsense_callback)
        self.motor_sub = self.session.declare_subscriber("marcsrover/motor", self.motor_callback)

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
        self.motor_sub.undeclare()
        self.session.close()

        dpg.destroy_context()

    def lidar_callback(self, sample):
        lidar_scale = dpg.get_value("LiDAR Scale")

        lidar = LidarScan.deserialize(sample.value.payload)

        dpg.delete_item(self.lidar_canvas)
        with dpg.drawlist(width=640, height=480, parent="LiDAR") as self.lidar_canvas:
            radius = 190

            dpg.draw_circle(center=(320, 230), radius=radius, color=(255, 255, 255, 255), thickness=1)
            dpg.draw_circle(center=(320, 230), radius=5, color=(255, 0, 0, 255), thickness=5)

            for i in range(0, 360, 30):
                x = 320 + radius * np.cos(np.radians(i))
                y = 230 + radius * np.sin(np.radians(i))
                dpg.draw_line((320, 230), (x, y), color=(255, 255, 255, 255), thickness=1)

                text_x = 320 + (radius + 20) * np.cos(np.radians(i)) - i * 20/360
                text_y = 230 + (radius + 20) * np.sin(np.radians(i)) - i * 20/360

                dpg.draw_text((text_x, text_y), str(i), color=(255, 255, 255, 255), size=16)

            for i in range (len(lidar.angles)):
                angle = lidar.angles[i]
                distance = lidar.distances[i]

                x = 320 + distance * np.cos(np.radians(angle)) * lidar_scale / 200
                y = 230 + distance * np.sin(np.radians(angle)) * lidar_scale / 200

                if np.sqrt((x - 320) ** 2 + (y - 230) ** 2) > radius:
                    continue

                dpg.draw_circle((int(x), int(y)), 1, color=(0, 0, 255, 255), thickness=5)

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

    def motor_callback(self, sample):
        motor = Motor.deserialize(sample.value.payload)

        dpg.set_value("Steering", motor.steering)
        dpg.set_value("Speed", motor.speed)
        dpg.set_value("Gear", motor.gear)


    def ctrl_c_signal(self, signum, frame):
        # Stop the node

        self.mutex.acquire()
        self.running = False
        self.mutex.release()

        # Put your cleanup code here

if __name__ == "__main__":
    monitoring = Monitoring()
    monitoring.run()
