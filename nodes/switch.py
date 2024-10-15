import signal
import zenoh
import time

class SwitchController:
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
        self.stop_handler = self.session.declare_subscriber("marcsrover/stop", self.handle_zenoh_stop)

    def run(self):
        while self.running:
            time.sleep(1)

        print("Switch Controller Stopped")
        exit(1)

    def stop(self, signum, frame):
        pass

    def handle_zenoh_stop(self, sample):
        print ("Stopping Switch Controller")
        self.running = False

if __name__ == "__main__":
    controller = SwitchController()
    controller.run()
