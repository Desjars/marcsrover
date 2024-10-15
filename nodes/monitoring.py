import signal
import time
import threading

import zenoh

import dearpygui.dearpygui as dpg

class Monitoring:
    def __init__(self):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.ctrl_c_signal)
        signal.signal(signal.SIGTERM, self.ctrl_c_signal)

        self.running = True
        self.mutex = threading.Lock()

        # Create node variables

        self.width = 640
        self.height = 480

        dpg.create_context()
        dpg.create_viewport(title='MARCSRover', width=self.width, height=self.height)
        dpg.setup_dearpygui()

        with dpg.window(tag="LiDAR"):
            pass

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/subs
        self.stop_handler = self.session.declare_publisher("marcsrover/stop")
        self.lidar_sub = self.session.declare_subscriber("marcsrover/lidar", self.lidar_callback)

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

        dpg.destroy_context()
        self.close()

    def close(self):
        self.stop_handler.put([])
        self.stop_handler.undeclare()
        self.session.close()

    def lidar_callback(self, sample):
        dpg.draw_rectangle((200, 200), (300, 300), parent="LiDAR", color=(255, 255, 0, 255), fill=(255, 0, 0, 255))

    def ctrl_c_signal(self, signum, frame):
        # Stop the node

        self.mutex.acquire()
        self.running = False
        self.mutex.release()

        # Put your cleanup code here

if __name__ == "__main__":
    monitoring = Monitoring()
    monitoring.run()
