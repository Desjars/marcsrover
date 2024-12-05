import cv2

import numpy as np
import dearpygui.dearpygui as dpg


from marcsrover.message import D435I
from marcsrover.common.realsense_depth import XY8_to_BGR8


def realsense_draw(sample: D435I) -> None:
    rgb = cv2.imdecode(
        np.frombuffer(bytes(sample.rgb), dtype=np.uint8), cv2.IMREAD_COLOR
    )
    depth = XY8_to_BGR8(
        np.frombuffer(bytes(sample.depth), dtype=np.uint8).reshape((240, 320, 2))
    )

    rgb, depth = cv2.resize(rgb, (480, 360)), cv2.resize(depth, (480, 360))
    rgb, depth = (
        cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR),
        cv2.cvtColor(depth, cv2.COLOR_RGB2BGR),
    )

    rgb, depth = (
        cv2.cvtColor(rgb, cv2.COLOR_RGB2RGBA),
        cv2.cvtColor(depth, cv2.COLOR_RGB2RGBA),
    )

    frame = np.zeros((720, 1024, 4))

    frame[:360, 272 : 480 + 272] = rgb
    frame[360:, 272 : 480 + 272] = depth

    frame = np.asarray(frame, dtype=np.float32)
    frame = np.true_divide(frame, 255.0)

    try:
        dpg.set_value("visualizer", frame)
    except:
        print("ERROR")
