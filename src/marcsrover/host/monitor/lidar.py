import cv2

import numpy as np
import dearpygui.dearpygui as dpg

from marcsrover.message import LidarScan


def lidar_draw(sample: LidarScan) -> None:
    
    with open("Lidar.csv", "a") as file:
        file.write(f"{str(sample.distances).replace('[','').replace(']','')}\n")
        
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

        distance = distance * 0.2

        if distance > radius:
            continue

        x = center[0] + distance * np.cos(np.deg2rad(angle))
        y = center[1] + distance * np.sin(np.deg2rad(angle))

        cv2.circle(frame, (int(x), int(y)), 1, (0.0, 0.0, 1.0, 1.0), 2)

    angles = np.array(sample.angles)
    indices = np.where((angles >= 350) | (angles <= 10))
    distances = np.array(sample.distances)[indices]
    mean = np.mean(distances) / 1000

    indices1 = np.where((angles >= 45) & (angles <= 90))
    indices2 = np.where((angles >= 270) & (angles <= 315))

    distances1 = np.array(sample.distances)[indices1]
    distances2 = np.array(sample.distances)[indices2]

    mean1 = np.mean(distances1) / 1000
    mean2 = np.mean(distances2) / 1000

    angle_indicator = mean1 - mean2

    cv2.putText(
        frame,
        f"Mean: {mean:.2f}m",
        (10, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (1.0, 1.0, 1.0, 1.0),
        1,
    )

    cv2.putText(
        frame,
        f"Mean1: {mean1:.2f}m",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (1.0, 1.0, 1.0, 1.0),
        1,
    )

    cv2.putText(
        frame,
        f"Mean2: {mean2:.2f}m",
        (10, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (1.0, 1.0, 1.0, 1.0),
        1,
    )

    cv2.putText(
        frame,
        f"Angle: {angle_indicator:.2f}m",
        (10, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (1.0, 1.0, 1.0, 1.0),
        1,
    )

    try:
        dpg.set_value("visualizer", frame)
    except:
        print("ERROR")
