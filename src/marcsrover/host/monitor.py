import zenoh
import threading
import json

class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5("connect/endpoints", json.dumps(["udp/0.0.0.0:7447"]))
        self.zenoh_config.insert_json5("listen/endpoints", json.dumps(["udp/127.0.0.1:0"]))

    def run (self, stop_event: threading.Event) -> None:
        with zenoh.open(self.zenoh_config) as session:
            while not stop_event.is_set():
                pass

            session.close()
        print('Monitor node stopped')

def launch_node(stop_event: threading.Event) -> None:
    node = Node()

    node.run(stop_event)
