from marcsrover.arguments import lidar_args, main_args, rover_args


def main_host() -> None:
    from marcsrover.host import run as run_host

    run_host(main_args())


def main_car() -> None:
    from marcsrover.car import run as run_car

    run_car(main_args())


def inner_monitor() -> None:
    from marcsrover.host.monitor import launch_node as launch_monitor

    launch_monitor()


def inner_joystick_controller() -> None:
    from marcsrover.host.joystick_controller import (
        launch_node as launch_joystick_controller,
    )

    launch_joystick_controller()


def inner_keyboard_controller() -> None:
    from marcsrover.host.keyboard_controller import (
        launch_node as launch_keyboard_controller,
    )

    launch_keyboard_controller()


def inner_opencv_camera() -> None:
    from marcsrover.common.opencv_camera import launch_node as launch_opencv_camera

    launch_opencv_camera()


def inner_lidar() -> None:
    from marcsrover.car.lidar import launch_node as launch_lidar

    launch_lidar(lidar_args())


def inner_realsense() -> None:
    from marcsrover.car.realsense import launch_node as launch_realsense

    launch_realsense()


def inner_rover() -> None:
    from marcsrover.car.rover import launch_node as launch_rover

    launch_rover(rover_args())


def inner_imu() -> None:
    from marcsrover.car.imu import launch_node as launch_imu

    launch_imu()


def inner_auto_pilot() -> None:
    from marcsrover.host.auto_pilot import launch_node as launch_auto_pilot

    launch_auto_pilot()
