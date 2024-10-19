import signal
import time
import threading

import zenoh

import numpy as np

from message import JoyStickController, Motor

class MotorControl:
    def __init__(self):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.ctrl_c_signal)
        signal.signal(signal.SIGTERM, self.ctrl_c_signal)

        self.running = True
        self.mutex = threading.Lock()

        # Create node variables
        self.steering = 0
        self.speed = 0
        self.gear = 5

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/sub
        self.stop_handler = self.session.declare_subscriber("marcsrover/stop", self.zenoh_stop_signal)
        self.controller_sub = self.session.declare_subscriber("marcsrover/controller", self.controller_callback)
        self.motor_pub = self.session.declare_publisher("marcsrover/motor")

    def run(self):
        while True:
            # Check if the node should stop

            self.mutex.acquire()
            running = self.running
            self.mutex.release()

            if not running:
                break

            # Put your update code here

            time.sleep(1)

        self.close()

    def close(self):
        self.stop_handler.undeclare()
        self.controller_sub.undeclare()
        self.motor_pub.undeclare()
        self.session.close()

    def controller_callback(self, sample):
        controller = JoyStickController.deserialize(sample.value.payload)

        steering_x = controller.axis[1]
        steering_y = controller.axis[0]
        self.steering = np.arctan2(steering_y, 1 - steering_x) * 180 / np.pi

        dec = controller.buttons[6]
        inc = controller.buttons[7]

        if dec and self.gear >=2:
            self.gear -= 1
        if inc and self.gear <= 9:
            self.gear += 1

        self.speed = -controller.axis[3] * (self.gear * 400)

        motor = Motor(speed=self.speed, steering=self.steering, gear=self.gear)
        self.motor_pub.put(Motor.serialize(motor))


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
    node = MotorControl()
    node.run()
