import signal
import time
import threading

import pygame
from pygame.constants import JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
import zenoh

from message import JoyStickController

class Controller:
    def __init__(self):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.ctrl_c_signal)
        signal.signal(signal.SIGTERM, self.ctrl_c_signal)

        self.running = True
        self.mutex = threading.Lock()

        # Create node variables
        pygame.init()
        pygame.event.set_blocked((MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN))

        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("This program only works with at least one joystick plugged in. No joysticks were detected.")
            exit(1)

        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

        self.axis = []
        for i in range(self.joy.get_numaxes()):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.joy.get_numballs()):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.joy.get_numbuttons()):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.joy.get_numhats()):
            self.hat.append(self.joy.get_hat(i))

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/sub
        self.stop_handler = self.session.declare_subscriber("marcsrover/stop", self.zenoh_stop_signal)

        self.controller_pub = self.session.declare_publisher("marcsrover/controller")

    def run(self):
        while True:
            # Check if the node should stop

            self.mutex.acquire()
            running = self.running
            self.mutex.release()

            if not running:
                break

            # Put your update code here

            events = pygame.event.get()

            num_events = len(events)
            if num_events == 0:
                continue

            for event in events:
                if event.type == pygame.QUIT:
                    break
                elif event.type == JOYAXISMOTION:
                    self.axis[event.axis] = event.value
                elif event.type == JOYBALLMOTION:
                    self.ball[event.ball] = event.rel
                elif event.type == JOYHATMOTION:
                    self.hat[event.hat] = event.value
                elif event.type == JOYBUTTONUP:
                    self.button[event.button] = 0
                elif event.type == JOYBUTTONDOWN:
                    self.button[event.button] = 1

            joystick = JoyStickController(axes=self.axis, buttons=self.button, balls=self.ball)
            self.controller_pub.put(JoyStickController.serialize(joystick))

        self.close()

    def close(self):
        self.stop_handler.undeclare()
        self.controller_pub.undeclare()
        self.session.close()
        pygame.quit()

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
    controller = Controller()
    controller.run()
