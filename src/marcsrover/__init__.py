from marcsrover.host import run as run_host
from marcsrover.car import run as run_car

import sys


def main_host() -> None:
    address_to_connect_to = sys.argv[1] if len(sys.argv) > 1 else None

    run_host(address_to_connect_to)


def main_car() -> None:
    address_to_listen_on = sys.argv[1] if len(sys.argv) > 1 else None

    run_car(address_to_listen_on)


def main_realsense() -> None:
    # Note: I'm trying to avoid this, and try to build librealsense and provide a special wheel for RB5 so it will be compatible
    # with the python of this project
    import subprocess

    command = "/home/.realsense/bin/python ~/marcsrover/src/marcsrover/car/realsense.py"

    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        print("Command executed successfully.")
        print("Standard Output:", result.stdout)
        print("Standard Error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error while executing the command.")
        print("Return Code:", e.returncode)
        print("Error:", e.stderr)
