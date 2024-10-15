import signal
import time
import threading

import zenoh

class Monitoring:
    def __init__(self):

        # Register signal handlers
        signal.signal(signal.SIGINT, self.ctrl_c_signal)
        signal.signal(signal.SIGTERM, self.ctrl_c_signal)

        self.running = True
        self.mutex = threading.Lock()

        # Create monitoring variables

        # Create zenoh session
        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        # Create zenoh pub/subs
        self.stop_handler = self.session.declare_publisher("marcsrover/stop")

    def run(self):
        while True:
            # Check if the node should stop

            self.mutex.acquire()
            running = self.running
            self.mutex.release()

            if not running:
                break

            # Put your update code here

            time.sleep(1)

        self.close()

    def close(self):
        self.stop_handler.undeclare()
        self.session.close()

    def ctrl_c_signal(self, signum, frame):
        # Stop the node

        self.mutex.acquire()
        self.running = False
        self.mutex.release()

        self.stop_handler.put([])

        # Put your cleanup code here

if __name__ == "__main__":
    monitoring = Monitoring()
    monitoring.run()
