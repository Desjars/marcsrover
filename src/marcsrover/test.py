import zenoh
import json

zenoh.init_log_from_env_or("info")

config = zenoh.Config.from_json5("{}")
config.insert_json5("connect/endpoints", json.dumps(["udp/10.0.0.5:7447"]))
config.insert_json5("listen/endpoints", json.dumps(["udp/0.0.0.0:7447"]))
config.insert_json5("scouting/multicast/enabled", json.dumps(False))
config.insert_json5("scouting/gossip/enabled", json.dumps(True))

with zenoh.open(config) as session:
    config2 = zenoh.Config.from_json5("{}")
    config2.insert_json5("connect/endpoints", json.dumps(["udp/127.0.0.1:7447"]))
    config2.insert_json5("listen/endpoints", json.dumps(["udp/0.0.0.0:0"]))
    config2.insert_json5("scouting/multicast/enabled", json.dumps(False))
    config2.insert_json5("scouting/gossip/enabled", json.dumps(True))

    with zenoh.open(config2) as session2:
        session2.put("test", "azihdaihzdahz")

        import time

        time.sleep(1)
