import os

import sys
import pygame
from pygame.constants import JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, VIDEORESIZE


class joystick_handler(object):
    def __init__(self, id):
        self.id = id
        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()

        self.numaxes    = self.joy.get_numaxes()
        self.numballs   = self.joy.get_numballs()
        self.numbuttons = self.joy.get_numbuttons()
        self.numhats    = self.joy.get_numhats()

        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.numballs):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))


class input_test(object):
    def init(self):
        pygame.init()
        pygame.event.set_blocked((MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN))

        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("This program only works with at least one joystick plugged in. No joysticks were detected.")
            self.quit(1)

        self.joy = joystick_handler(0)

    def run(self):
        while True:
            for event in [pygame.event.wait(), ] + pygame.event.get():
                # QUIT             none
                # MOUSEMOTION      pos, rel, buttons
                # MOUSEBUTTONUP    pos, button
                # MOUSEBUTTONDOWN  pos, button
                # JOYAXISMOTION    joy, axis, value
                # JOYBALLMOTION    joy, ball, rel
                # JOYHATMOTION     joy, hat, value
                # JOYBUTTONUP      joy, button
                # JOYBUTTONDOWN    joy, button
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == JOYAXISMOTION:
                    self.joy.axis[event.axis] = event.value
                    print(event.joy)
                elif event.type == JOYBALLMOTION:
                    self.joy.ball[event.ball] = event.rel
                elif event.type == JOYHATMOTION:
                    self.joy.hat[event.hat] = event.value
                elif event.type == JOYBUTTONUP:
                    self.joy.button[event.button] = 0
                elif event.type == JOYBUTTONDOWN:
                    self.joy.button[event.button] = 1



    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)


if __name__ == "__main__":
    program = input_test()
    program.init()
    program.run()  # This function should never return
