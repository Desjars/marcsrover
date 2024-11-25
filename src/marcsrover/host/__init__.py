import zenoh
import json
import subprocess
import signal
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


def run(address_to_connect_to) -> None:
    zenoh.init_log_from_env_or("info")

    router_config: zenoh.Config = zenoh.Config.from_json5("{}")

    router_config.insert_json5("listen/endpoints", json.dumps(["udp/127.0.0.1:7447"]))
    router_config.insert_json5("scouting/multicast/enabled", json.dumps(False))
    if address_to_connect_to is not None:
        router_config.insert_json5(
            "connect/endpoints", json.dumps([f"udp/{address_to_connect_to}:7445"])
        )

    with zenoh.open(router_config) as session:
        signal.signal(signal.SIGINT, signal_handler)

        try:
            processes.append(
                subprocess.Popen(["uv", "run", "src/marcsrover/host/monitor.py"])
            )
            processes.append(
                subprocess.Popen(
                    ["uv", "run", "src/marcsrover/common/opencv_camera.py"]
                )
            )

            print("Processes started. Press CTRL+C to terminate.")

            for process in processes:
                process.wait()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            terminate_processes()

        session.close()
