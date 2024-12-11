import zenoh
import cv2
import numpy as np

import dearpygui.dearpygui as dpg

from marcsrover.message import AutoPilotConfig, LidarScan


def callback(session: zenoh.Session) -> None:
    bytes = AutoPilotConfig(
        min_speed=dpg.get_value("min_speed"),
        max_speed=dpg.get_value("max_speed"),
        back_treshold=dpg.get_value("back_treshold"),
        fwd_treshold=dpg.get_value("fwd_treshold"),
        steering_1_treshold=dpg.get_value("steering_1_treshold"),
        steering_2_treshold=dpg.get_value("steering_2_treshold"),
        steering_1_min_angle=dpg.get_value("steering_1_min_angle"),
        steering_1_max_angle=dpg.get_value("steering_1_max_angle"),
        steering_2_min_angle=dpg.get_value("steering_2_min_angle"),
        steering_2_max_angle=dpg.get_value("steering_2_max_angle"),
        enable=dpg.get_value("enable"),
    ).serialize()

    session.put("marcsrover/autopilot/config", bytes)


def init_autopilot(session: zenoh.Session) -> None:
    with dpg.window(
        label="autopilot", width=256, height=720 - 128 - 256, pos=(1024, 128 + 256)
    ):
        dpg.add_slider_int(
            label="min_speed",
            tag="min_speed",
            width=150,
            min_value=0,
            max_value=3000,
            default_value=0,
        )
        dpg.add_slider_int(
            label="max_speed",
            tag="max_speed",
            width=150,
            min_value=0,
            max_value=3000,
            default_value=0,
        )

        dpg.add_slider_float(
            label="back_treshold",
            tag="back_treshold",
            width=150,
            min_value=0,
            max_value=4,
            default_value=0.5,
        )
        dpg.add_slider_float(
            label="fwd_treshold",
            tag="fwd_treshold",
            width=150,
            min_value=0,
            max_value=4,
            default_value=1.5,
        )

        dpg.add_slider_float(
            label="steering_1_treshold",
            tag="steering_1_treshold",
            width=150,
            min_value=0,
            max_value=1,
            default_value=0.3,
        )

        dpg.add_slider_float(
            label="steering_2_treshold",
            tag="steering_2_treshold",
            width=150,
            min_value=0,
            max_value=1,
            default_value=0.3,
        )

        dpg.add_slider_int(
            label="steering_1_min_angle",
            tag="steering_1_min_angle",
            width=150,
            min_value=0,
            max_value=90,
            default_value=45,
        )
        dpg.add_slider_int(
            label="steering_1_max_angle",
            tag="steering_1_max_angle",
            width=150,
            min_value=0,
            max_value=90,
            default_value=90,
        )

        dpg.add_slider_int(
            label="steering_2_min_angle",
            tag="steering_2_min_angle",
            width=150,
            min_value=0,
            max_value=90,
            default_value=15,
        )
        dpg.add_slider_int(
            label="steering_2_max_angle",
            tag="steering_2_max_angle",
            width=150,
            min_value=0,
            max_value=90,
            default_value=45,
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

    steering_1_min = dpg.get_value("steering_1_min_angle")
    steering_1_max = dpg.get_value("steering_1_max_angle")

    steering_2_min = dpg.get_value("steering_2_min_angle")
    steering_2_max = dpg.get_value("steering_2_max_angle")

    back_treshold = dpg.get_value("back_treshold")
    fwd_treshold = dpg.get_value("fwd_treshold")

    # draw line for tresholds
    cv2.line(
        frame,
        (
            center[0] + int(back_treshold * 1000 * 0.2),
            center[1] - 15,
        ),
        (
            center[0] + int(back_treshold * 1000 * 0.2),
            center[1] + 15,
        ),
        (0.0, 0.0, 1.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        (
            center[0] + int(fwd_treshold * 1000 * 0.2),
            center[1] - 15,
        ),
        (
            center[0] + int(fwd_treshold * 1000 * 0.2),
            center[1] + 15,
        ),
        (0.0, 1.0, 1.0, 1.0),
        4,
    )

    # draw steering range
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(steering_1_min))),
            int(center[1] + radius * np.sin(np.deg2rad(steering_1_min))),
        ),
        (1.0, 0.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(steering_1_max))),
            int(center[1] + radius * np.sin(np.deg2rad(steering_1_max))),
        ),
        (1.0, 0.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(360 - steering_1_max))),
            int(center[1] + radius * np.sin(np.deg2rad(360 - steering_1_max))),
        ),
        (1.0, 0.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(360 - steering_1_min))),
            int(center[1] + radius * np.sin(np.deg2rad(360 - steering_1_min))),
        ),
        (1.0, 0.0, 0.0, 1.0),
        4,
    )

    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(steering_2_min))),
            int(center[1] + radius * np.sin(np.deg2rad(steering_2_min))),
        ),
        (0.0, 1.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(steering_2_max))),
            int(center[1] + radius * np.sin(np.deg2rad(steering_2_max))),
        ),
        (0.0, 1.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(360 - steering_2_max))),
            int(center[1] + radius * np.sin(np.deg2rad(360 - steering_2_max))),
        ),
        (0.0, 1.0, 0.0, 1.0),
        4,
    )
    cv2.line(
        frame,
        center,
        (
            int(center[0] + radius * np.cos(np.deg2rad(360 - steering_2_min))),
            int(center[1] + radius * np.sin(np.deg2rad(360 - steering_2_min))),
        ),
        (0.0, 1.0, 0.0, 1.0),
        4,
    )

    angles = np.array(sample.angles)

    indices1 = np.where(
    (angles >= steering_1_min)
    & (angles <= steering_1_max)
    )
    indices2 = np.where(
    (angles >= 360 - steering_1_max)
    & (angles <= 360 - steering_1_min)
    )

    distances1 = np.array(sample.distances)[indices1]
    distances2 = np.array(sample.distances)[indices2]

    mean1 = np.mean(distances1) / 1000
    mean2 = np.mean(distances2) / 1000
    mean3 = mean1 - mean2
    # keep 2 decimal places
    cv2.putText(frame, f"RED right: {mean1:.2f}", (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (1.0, 0.0, 0.0, 1.0), 2)
    cv2.putText(frame, f"RED left: {mean2:.2f}", (40, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (1.0, 0.0, 0.0, 1.0), 2)
    cv2.putText(frame, f"RED diff: {mean3:.2f}", (40, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (1.0, 0.0, 0.0, 1.0), 2)

    indices1 = np.where(
    (angles >= steering_2_min)
    & (angles <= steering_2_max)
    )
    indices2 = np.where(
    (angles >= 360 - steering_2_max)
    & (angles <= 360 - steering_2_min)
    )

    distances1 = np.array(sample.distances)[indices1]
    distances2 = np.array(sample.distances)[indices2]

    mean1 = np.mean(distances1) / 1000
    mean2 = np.mean(distances2) / 1000
    mean3 = mean1 - mean2
    # keep 2 decimal places
    cv2.putText(frame, f"GREEN right: {mean1:.2f}", (40, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0.0, 1.0, 0.0, 1.0), 2)
    cv2.putText(frame, f"GREEN left: {mean2:.2f}", (40, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0.0, 1.0, 0.0, 1.0), 2)
    cv2.putText(frame, f"GREEN diff: {mean3:.2f}", (40, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0.0, 1.0, 0.0, 1.0), 2)


    try:
        dpg.set_value("visualizer", frame)
    except:
        print("ERROR")
