import serial
import time

with serial.Serial("/dev/ttyACM0", 115200, timeout=1) as ser:
    ser.write(("s05000" + "\n").encode("utf-8"))  # Envoi du message avec '\n'
    time.sleep(2)
    ser.write(("s02000" + "\n").encode("utf-8"))  # Envoi du message avec '\n'
    time.sleep(2)
