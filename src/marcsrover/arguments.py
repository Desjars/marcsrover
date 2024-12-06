import argparse


def main_args():
    parser = argparse.ArgumentParser(description="Configuration of the MarcsRover.")

    parser.add_argument(
        "--ip",
        type=str,
        default="127.0.0.1",
        help="IP address to either listen on or connect to. Should be the same for both the host and the car.",
    )

    parser.add_argument(
        "--servo-port",
        type=str,
        default="/dev/tty_SERVO",
        help="Serial port for the connection to the servo motor.",
    )

    parser.add_argument(
        "--microcontroller-port",
        type=str,
        default="/dev/tty_STM32",
        help="Serial port for the connection to the microcontroller.",
    )

    parser.add_argument(
        "--lidar-port",
        type=str,
        default="/dev/tty_LIDAR",
        help="Serial port for the connection to the LiDAR.",
    )

    return parser.parse_args()


def lidar_args():
    parser = argparse.ArgumentParser(description="Configuration of the LiDAR.")

    parser.add_argument(
        "--lidar-port",
        type=str,
        default="/dev/ttyUSB0",
        help="Serial port for the connection to the LiDAR.",
    )

    return parser.parse_args()


def rover_args():
    parser = argparse.ArgumentParser(description="Configuration of the rover.")

    parser.add_argument(
        "--servo-port",
        type=str,
        default="/dev/ttyACM1",
        help="Serial port for the connection to the servo motor.",
    )

    parser.add_argument(
        "--microcontroller-port",
        type=str,
        default="/dev/ttyACM0",
        help="Serial port for the connection to the microcontroller.",
    )

    return parser.parse_args()
