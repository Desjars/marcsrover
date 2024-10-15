import signal
import time
import threading

import zenoh

from pyrplidar import PyRPlidar
from message import LidarScan

class Lidar:
    def __init__(self, port='/dev/tty.usbserial-8440', bauderate=256000, timeout=3, pwm=500):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.ctrl_c_signal)
        signal.signal(signal.SIGTERM, self.ctrl_c_signal)

        self.running = True
        self.mutex = threading.Lock()

        # Create monitoring variables
        self.lidar = PyRPlidar()
        self.lidar.connect(port, bauderate, timeout)

        # The LiDAR may not have been stopped properly, so we need to reset it

        self.lidar.set_motor_pwm(0)
        self.lidar.stop()
        self.lidar.disconnect()

        time.sleep(2) # Wait for the lidar to stop

        # Now we can start

        self.lidar.connect(port, bauderate, timeout)
        self.lidar.set_motor_pwm(pwm)

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/sub
        self.stop_handler = self.session.declare_subscriber("marcsrover/stop", self.zenoh_stop_signal)
        self.lidar_publisher = self.session.declare_publisher("marcsrover/lidar")

    def run(self):
        time.sleep(2) # Wait for the lidar to start
        scan_generator = self.lidar.start_scan()

        qualities = []
        angles = []
        distances = []

        for count, scan in enumerate(scan_generator()):
            self.mutex.acquire()
            running = self.running
            self.mutex.release()

            if not running:
                break

            quality = scan.quality
            angle = scan.angle
            distance = scan.distance

            if angle < 1: # When the angle is less than 1, we have a full tour scan
                lidar_scan = LidarScan(qualities=qualities, angles=angles, distances=distances)
                self.lidar_publisher.put(LidarScan.serialize(lidar_scan))

                qualities = []
                angles = []
                distances = []

            qualities.append(quality)
            angles.append(angle)
            distances.append(distance)

        self.close()

    def close(self):
        self.stop_handler.undeclare()
        self.lidar_publisher.undeclare()
        self.session.close()

        self.lidar.set_motor_pwm(0)
        self.lidar.stop()
        self.lidar.disconnect()

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
    node = Lidar(port='/dev/tty.usbserial-8440', bauderate=256000, timeout=3, pwm=500)
    node.run()
