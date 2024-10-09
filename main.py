import zenoh

config = zenoh.Config.from_file("config.json")
session = zenoh.open(config)

session.put("marcsrover/temperature", f"{25}")
