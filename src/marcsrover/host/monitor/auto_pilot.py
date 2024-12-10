import zenoh
import cv2
import numpy as np

import dearpygui.dearpygui as dpg

from marcsrover.message import AutoPilotConfig, LidarScan


def callback(session: zenoh.Session) -> None:
    bytes = AutoPilotConfig(
        min_speed=dpg.get_value("min_speed"),
        max_speed=dpg.get_value("max_speed"),
        back_speed=dpg.get_value("back_speed"),
        steering=dpg.get_value("steering"),
        back_treshold=dpg.get_value("back_treshold"),
        fwd_treshold=dpg.get_value("fwd_treshold"),
        steering_treshold=dpg.get_value("steering_treshold"),
        steering_min_angle=dpg.get_value("steering_min_angle"),
        steering_max_angle=dpg.get_value("steering_max_angle"),
        enable=dpg.get_value("enable"),
    ).serialize()

    session.put("marcsrover/autopilot/config", bytes)


def init_autopilot(session: zenoh.Session) -> None:
    with dpg.window(label="autopilot", width=256, height=720-128-256, pos=(1024, 128 + 256)):
        dpg.add_slider_int(
            label="min_speed",
            tag="min_speed",
            width=150,
            min_value=0,
            max_value=2000,
            default_value=0,
        )
        dpg.add_slider_int(
            label="max_speed",
            tag="max_speed",
            width=150,
            min_value=0,
            max_value=2000,
            default_value=0,
        )
        dpg.add_slider_int(
            label="back_speed",
            tag="back_speed",
            width=150,
            min_value=0,
            max_value=3000,
            default_value=0,
        )
        dpg.add_slider_int(
            label="steering",
            tag="steering",
            width=150,
            min_value=0,
            max_value=90,
            default_value=90,
        )
        dpg.add_slider_float(
            label="back_treshold",
            tag="back_treshold",
            width=150,
            min_value=0,
            max_value=2,
            default_value=0.5,
        )
        dpg.add_slider_float(
            label="fwd_treshold",
            tag="fwd_treshold",
            width=150,
            min_value=0,
            max_value=2,
            default_value=0.5,
        )
        dpg.add_slider_float(
            label="steering_treshold",
            tag="steering_treshold",
            width=150,
            min_value=0,
            max_value=2,
            default_value=0.5,
        )
        dpg.add_slider_int(
            label="steering_min_angle",
            tag="steering_min_angle",
            width=150,
            min_value=0,
            max_value=90,
            default_value=45,
        )
        dpg.add_slider_int(
            label="steering_max_angle",
            tag="steering_max_angle",
            width=150,
            min_value=0,
            max_value=90,
            default_value=90,
        )
        dpg.add_checkbox(label="enable", tag="enable", default_value=True)
        dpg.add_button(label="send", width=150, callback=lambda: callback(session))

def draw_auto_pilot(sample: LidarScan) -> None:
    center = (512, 380)
    radius = 300

    frame = np.zeros((720, 1024, 4), dtype=np.float32)

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

    steering_min = dpg.get_value("steering_min_angle")
    steering_max = dpg.get_value("steering_max_angle")

    # draw steering range
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(steering_min))),
            int(center[1] + radius * np.sin(np.deg2rad(steering_min))),
        ),
        (1.0, 0.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(steering_max))),
            int(center[1] + radius * np.sin(np.deg2rad(steering_max))),
        ),
        (1.0, 0.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(360 - steering_max))),
            int(center[1] + radius * np.sin(np.deg2rad(360 - steering_max))),
        ),
        (1.0, 0.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(360 - steering_min))),
            int(center[1] + radius * np.sin(np.deg2rad(360 - steering_min))),
        ),
        (1.0, 0.0, 0.0, 1.0),
        4,
    )

    angles = np.array(sample.angles)
    indices = np.where((angles >= 350) | (angles <= 10))
    distances = np.array(sample.distances)[indices]
    mean = np.mean(distances) / 1000

    indices1 = np.where((angles >= steering_min) & (angles <= steering_max))
    indices2 = np.where((angles >= 360 - steering_max) & (angles <= 360 - steering_min))

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
