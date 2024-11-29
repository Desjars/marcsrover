import sys


def main_host() -> None:
    from marcsrover.host import run as run_host

    address_to_connect_to = sys.argv[1] if len(sys.argv) > 1 else None

    run_host(address_to_connect_to)


def main_car() -> None:
    from marcsrover.car import run as run_car

    address_to_listen_on = sys.argv[1] if len(sys.argv) > 1 else None

    run_car(address_to_listen_on)


def inner_monitor() -> None:
    from marcsrover.host.monitor import launch_node as launch_monitor

    launch_monitor()


def inner_joystick_controller() -> None:
    from marcsrover.host.joystick_controller import (
        launch_node as launch_joystick_controller,
    )

    launch_joystick_controller()


def inner_opencv_camera() -> None:
    from marcsrover.common.opencv_camera import launch_node as launch_opencv_camera

    launch_opencv_camera()


def inner_lidar() -> None:
    from marcsrover.car.lidar import launch_node as launch_lidar

    launch_lidar()


def inner_realsense() -> None:
    from marcsrover.car.realsense import launch_node as launch_realsense

    launch_realsense()


def inner_rover() -> None:
    from marcsrover.car.rover import launch_node as launch_rover

    launch_rover()
