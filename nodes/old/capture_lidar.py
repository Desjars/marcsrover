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
        print(scan)

        if count == 20: break # Stop the scan after 20 scans


    # Stop the motor and disconnect the LiDAR
    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()


if __name__ == "__main__":
    simple_scan()

"""
An example of a simple scan using the PyRPlidar library :

{'start_flag': False, 'quality': 15, 'angle': 97.546875, 'distance': 837.0} -> count = 0
{'start_flag': False, 'quality': 15, 'angle': 98.3125, 'distance': 838.0} -> count = 1
{'start_flag': False, 'quality': 15, 'angle': 99.203125, 'distance': 837.75} -> count = 2
{'start_flag': False, 'quality': 15, 'angle': 100.0, 'distance': 838.5} -> count = 3
{'start_flag': False, 'quality': 15, 'angle': 100.78125, 'distance': 839.25} -> count = 4
{'start_flag': False, 'quality': 15, 'angle': 101.625, 'distance': 839.75} ...
{'start_flag': False, 'quality': 15, 'angle': 102.40625, 'distance': 839.5}
{'start_flag': False, 'quality': 15, 'angle': 103.328125, 'distance': 840.25}
{'start_flag': False, 'quality': 15, 'angle': 104.15625, 'distance': 841.75}
{'start_flag': False, 'quality': 15, 'angle': 105.03125, 'distance': 843.0}
{'start_flag': False, 'quality': 0, 'angle': 112.046875, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 112.875, 'distance': 0.0}
{'start_flag': False, 'quality': 15, 'angle': 106.625, 'distance': 1634.75}
{'start_flag': False, 'quality': 7, 'angle': 107.3125, 'distance': 1662.75}
{'start_flag': False, 'quality': 15, 'angle': 108.09375, 'distance': 1689.0}
{'start_flag': False, 'quality': 15, 'angle': 116.09375, 'distance': 0.0}
{'start_flag': False, 'quality': 15, 'angle': 109.640625, 'distance': 1999.0}
{'start_flag': False, 'quality': 0, 'angle': 117.71875, 'distance': 0.0}
{'start_flag': False, 'quality': 15, 'angle': 111.296875, 'distance': 1949.5}
{'start_flag': False, 'quality': 15, 'angle': 112.171875, 'distance': 1916.75}
{'start_flag': False, 'quality': 9, 'angle': 113.1875, 'distance': 1511.25}
{'start_flag': False, 'quality': 15, 'angle': 114.0, 'distance': 1508.0}
{'start_flag': False, 'quality': 15, 'angle': 114.8125, 'distance': 1539.0}
{'start_flag': False, 'quality': 15, 'angle': 115.578125, 'distance': 1605.0}
{'start_flag': False, 'quality': 15, 'angle': 116.390625, 'distance': 1641.75}
{'start_flag': False, 'quality': 15, 'angle': 117.1875, 'distance': 1795.5}
{'start_flag': False, 'quality': 15, 'angle': 118.03125, 'distance': 1778.75}
{'start_flag': False, 'quality': 15, 'angle': 118.890625, 'distance': 1757.0}
{'start_flag': False, 'quality': 15, 'angle': 119.640625, 'distance': 1741.5}
{'start_flag': False, 'quality': 15, 'angle': 120.515625, 'distance': 1723.75}
{'start_flag': False, 'quality': 15, 'angle': 121.34375, 'distance': 1702.75}
{'start_flag': False, 'quality': 15, 'angle': 122.1875, 'distance': 1699.0}
{'start_flag': False, 'quality': 11, 'angle': 122.96875, 'distance': 1718.5}
{'start_flag': False, 'quality': 0, 'angle': 130.96875, 'distance': 0.0}
{'start_flag': False, 'quality': 6, 'angle': 124.671875, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 132.625, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 133.453125, 'distance': 0.0}
{'start_flag': False, 'quality': 4, 'angle': 127.09375, 'distance': 1774.75}
{'start_flag': False, 'quality': 6, 'angle': 127.9375, 'distance': 1761.5}
{'start_flag': False, 'quality': 15, 'angle': 128.734375, 'distance': 1785.0}
{'start_flag': False, 'quality': 15, 'angle': 129.546875, 'distance': 1796.25}
{'start_flag': False, 'quality': 15, 'angle': 130.421875, 'distance': 1805.5}
{'start_flag': False, 'quality': 15, 'angle': 131.328125, 'distance': 1796.25}
{'start_flag': False, 'quality': 15, 'angle': 132.203125, 'distance': 1788.0}
{'start_flag': False, 'quality': 15, 'angle': 135.203125, 'distance': 463.0}
{'start_flag': False, 'quality': 15, 'angle': 136.140625, 'distance': 445.0}
{'start_flag': False, 'quality': 15, 'angle': 137.34375, 'distance': 433.25}
{'start_flag': False, 'quality': 15, 'angle': 138.265625, 'distance': 426.25}
{'start_flag': False, 'quality': 15, 'angle': 139.171875, 'distance': 422.25}
{'start_flag': False, 'quality': 15, 'angle': 140.015625, 'distance': 412.0}
{'start_flag': False, 'quality': 15, 'angle': 140.609375, 'distance': 410.25}
{'start_flag': False, 'quality': 15, 'angle': 141.625, 'distance': 410.25}
{'start_flag': False, 'quality': 15, 'angle': 142.375, 'distance': 414.75}
{'start_flag': False, 'quality': 8, 'angle': 147.65625, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 148.46875, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 149.296875, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 150.125, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 150.953125, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 151.78125, 'distance': 0.0}
{'start_flag': False, 'quality': 15, 'angle': 146.3125, 'distance': 0.0}
{'start_flag': False, 'quality': 15, 'angle': 147.046875, 'distance': 888.0}
{'start_flag': False, 'quality': 3, 'angle': 154.28125, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 155.109375, 'distance': 0.0}
{'start_flag': False, 'quality': 15, 'angle': 155.953125, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 156.765625, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 157.609375, 'distance': 0.0}
{'start_flag': False, 'quality': 15, 'angle': 150.9375, 'distance': 2946.0}
{'start_flag': False, 'quality': 0, 'angle': 159.265625, 'distance': 0.0}
{'start_flag': False, 'quality': 0, 'angle': 160.09375, 'distance': 0.0}
{'start_flag': False, 'quality': 6, 'angle': 154.046875, 'distance': 0.0}
{'start_flag': False, 'quality': 15, 'angle': 154.890625, 'distance': 1361.75}
{'start_flag': False, 'quality': 15, 'angle': 155.625, 'distance': 1357.25}
{'start_flag': False, 'quality': 15, 'angle': 156.484375, 'distance': 1399.0}
{'start_flag': False, 'quality': 15, 'angle': 157.25, 'distance': 1448.25}
{'start_flag': False, 'quality': 15, 'angle': 158.0, 'distance': 1501.0}
"""
