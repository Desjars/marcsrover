import signal
import time

import zenoh

class Monitoring:
    def __init__(self):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        self.running = True

        # Create monitoring variables

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh subscriber
        self.stop_handler = self.session.declare_publisher("marcsrover/stop")

    def run(self):
        while self.running:
            time.sleep(1)

    def stop(self, signum, frame):
        self.running = False
        self.stop_handler.put([])
        exit(1)

if __name__ == "__main__":
    monitoring = Monitoring()
    monitoring.run()
