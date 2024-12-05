import cv2

import numpy as np
import dearpygui.dearpygui as dpg

from marcsrover.message import LidarScan


def lidar_draw(sample: LidarScan) -> None:
    frame = np.zeros((720, 1024, 4))
    frame = np.asarray(frame, dtype=np.float32)

    center = (512, 380)
    radius = 300

    cv2.circle(frame, center, 5, (1.0, 0.0, 0.0, 1.0), 1)
    cv2.circle(frame, center, radius, (1.0, 1.0, 1.0, 1.0), 1)

    for i in range(0, 360, 30):
        angle = np.deg2rad(i)

        x = int(center[0] + radius * np.cos(angle))
        y = int(center[1] + radius * np.sin(angle))

        cv2.line(frame, center, (x, y), (1.0, 1.0, 1.0, 1.0), 1)

        x, y = x - len(str(i)) * 6, y + 2
        x, y = (
            x + np.cos(angle) * len(str(i)) * 6 + 10 * np.sign(np.cos(angle)),
            y + np.sin(angle) * len(str(i)) * 6 + 10 * np.sign(np.sin(angle)),
        )
        x, y = int(x), int(y)

        cv2.putText(
            frame,
            str(i),
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (1.0, 1.0, 1.0, 1.0),
            1,
        )

    for i in range(len(sample.angles)):
        angle = sample.angles[i]
        distance = sample.distances[i]

        if distance < 0 or distance > radius:
            continue

        x = center[0] + distance * np.cos(np.deg2rad(angle)) * 0.5
        y = center[1] + distance * np.sin(np.deg2rad(angle)) * 0.5

        cv2.circle(frame, (int(x), int(y)), 1, (0.0, 0.0, 1.0, 1.0), 1)

    try:
        dpg.set_value("visualizer", frame)
    except:
        print("ERROR")
