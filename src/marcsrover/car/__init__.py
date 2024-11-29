import zenoh
import signal
import json

import subprocess
import sys

processes = []


def terminate_processes():
    """Termine tous les processus enfants."""
    for process in processes:
        try:
            process.terminate()
        except subprocess.TimeoutExpired:
            process.kill()


def signal_handler(sig, frame):
    print("Termination signal received. Shutting down processes...")

    terminate_processes()

    sys.exit(0)


def run(address_to_listen_on) -> None:
    zenoh.init_log_from_env_or("info")

    router_config: zenoh.Config = zenoh.Config.from_json5("{}")

    endpoints = ["udp/0.0.0.0:7446"]

    if address_to_listen_on is not None:
        endpoints.append(f"udp/{address_to_listen_on}:7445")

    router_config.insert_json5("listen/endpoints", json.dumps(endpoints))
    router_config.insert_json5("scouting/gossip/enabled", json.dumps(True))
    router_config.insert_json5("scouting/multicast/enabled", json.dumps(False))

    with zenoh.open(router_config) as session:
        signal.signal(signal.SIGINT, signal_handler)

        try:
            # processes.append(subprocess.Popen(["uv", "run", "lidar"]))
            # processes.append(subprocess.Popen(["uv", "run", "realsense"]))
            processes.append(subprocess.Popen(["uv", "run", "rover"]))

            print("Processes started. Press CTRL+C to terminate.")

            for process in processes:
                process.wait()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            terminate_processes()

        session.close()
