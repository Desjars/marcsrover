import sys


def main_host() -> None:
    from marcsrover.host import run as run_host

    address_to_connect_to = sys.argv[1] if len(sys.argv) > 1 else None

    run_host(address_to_connect_to)


def main_car() -> None:
    from marcsrover.car import run as run_car

    address_to_listen_on = sys.argv[1] if len(sys.argv) > 1 else None

    run_car(address_to_listen_on)
