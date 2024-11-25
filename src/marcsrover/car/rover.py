import zenoh
import json


class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7446"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/0.0.0.0:0"])
        )
        self.zenoh_config.insert_json5("scouting/multicast/enabled", json.dumps(False))
        self.zenoh_config.insert_json5("scouting/gossip/enabled", json.dumps(True))

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                print("Rover Received KeyboardInterrupt")

            session.close()

        print("Rover Node stopped")


node = Node()
node.run()
