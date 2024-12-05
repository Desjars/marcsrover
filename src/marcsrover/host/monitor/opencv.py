import cv2

import numpy as np
import dearpygui.dearpygui as dpg

from marcsrover.message import BytesMessage


def opencv_draw(sample: BytesMessage) -> None:
    rgb = np.frombuffer(bytes(sample.data), dtype=np.uint8)

    rgb = cv2.imdecode(rgb, cv2.IMREAD_COLOR)
    rgb = cv2.resize(rgb, (640, 480))
    rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2RGBA)
    frame = np.zeros((720, 1024, 4))

    frame[120 : 480 + 120, 192 : 640 + 192] = rgb
    rgb = frame

    rgb = np.asarray(rgb, dtype=np.float32)
    rgb = np.true_divide(rgb, 255.0)

    try:
        dpg.set_value("visualizer", rgb)
    except:
        print("ERROR")
