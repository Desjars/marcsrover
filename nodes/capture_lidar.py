from pyrplidar import PyRPlidar
import time

# Start a scan
def simple_scan():
    # Create a PyRPlidar object
    lidar = PyRPlidar()

    # Connect the LiDAR to your computer and fill in the port (e.g COM3, COM4, etc. on windows)
    lidar.connect(port="/dev/tty.usbserial-8330", baudrate=256000, timeout=3)

    # Start the motor of the LiDAR
    lidar.set_motor_pwm(500)

    # Wait for the motor to reach its speed
    time.sleep(2)

    # Create a scan generator object
    scan_generator = lidar.force_scan()

    # Iterate over the scan generator, it will not stop until you stop it, for example with a break after a certain number of scans
    for count, scan in enumerate(scan_generator()):
        print(count, scan)

        if count == 20: break # Stop the scan after 20 scans


    # Stop the motor and disconnect the LiDAR
    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()


if __name__ == "__main__":
    simple_scan()
