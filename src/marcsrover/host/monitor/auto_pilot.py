import zenoh
import cv2
import numpy as np

import dearpygui.dearpygui as dpg

from marcsrover.message import AutoPilotConfig, LidarScan

from sklearn.cluster import DBSCAN


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

        dpg.add_checkbox(label="enable", tag="enable", default_value=False)
        dpg.add_button(label="send", width=150, callback=lambda: callback(session))


def draw_background(center, radius, frame) -> None:
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


def draw_auto_pilot(sample: LidarScan) -> None:
    frame = np.zeros((720, 1024, 4), dtype=np.float32)

    center = (512, 380)
    radius = 300
    scale = 0.1

    draw_background(center, radius, frame)

    distances = np.array(sample.distances)
    angles = np.array(sample.angles)

    indices = np.where(distances * scale < radius)
    distances = distances[indices]
    angles = angles[indices]

    x = center[0] + distances * scale * np.cos(np.deg2rad(angles))
    y = center[1] + distances * scale * np.sin(np.deg2rad(angles))

    points = np.vstack((x, y)).T

    for point in points:
        cv2.circle(frame, (int(point[0]), int(point[1])), 1, (0.0, 0.0, 1.0, 1.0), 2)

    indices = np.where(
        (angles >= 0) & (angles <= 90) | (angles >= 270) & (angles <= 360)
    )
    distances = distances[indices]
    angles = angles[indices]
    points = points[indices]

    local_means = np.array(
        [
            np.mean(
                np.concatenate(
                    [
                        distances[-5:],
                        distances,
                        distances[:5],
                    ]
                )[i : i + 2 * 5 + 1]
            )
            for i in range(len(distances))
        ]
    )

    disc = np.where(np.abs(distances - local_means) > 500)
    critical_points = points[disc]

    for point in critical_points:
        cv2.circle(frame, (int(point[0]), int(point[1])), 1, (1.0, 0.0, 0.0, 1.0), 2)

    if len(critical_points) >= 1:
        clusters = DBSCAN(eps=100, min_samples=1).fit(critical_points)

        for i in range(len(np.unique(clusters.labels_))):
            indices = np.where(clusters.labels_ == i)

            cluster = critical_points[indices]

            if len(cluster) < 2:
                continue

            x = int(np.mean(cluster[:, 0]))
            y = int(np.mean(cluster[:, 1]))

            cv2.circle(
                frame,
                (x, y),
                5,
                (0.0, 1.0, 0.0, 1.0),
                2,
            )

        if len(np.unique(clusters.labels_)) >= 2:
            mean = np.mean(critical_points, axis=0)

            cv2.circle(
                frame,
                (int(mean[0]), int(mean[1])),
                5,
                (1.0, 1.0, 0.0, 1.0),
                2,
            )

            cv2.polylines(
                frame,
                [
                    np.array(
                        [
                            center,
                            (
                                int(mean[0]),
                                int(mean[1]),
                            ),
                        ]
                    )
                ],
                False,
                (1.0, 1.0, 0.0, 1.0),
                2,
            )

    try:
        dpg.set_value("visualizer", frame)
    except:
        print("ERROR")


def draw_auto_pilot_2(sample: LidarScan) -> None:
    center = (512, 380)
    radius = 300

    frame = np.zeros((720, 1024, 4), dtype=np.float32)

    cv2.circle(frame, center, 5, (1.0, 0.0, 0.0, 1.0), 1)
    cv2.circle(frame, center, radius, (1.0, 1.0, 1.0, 1.0), 1)

    # post processing, keep only values with distances < 10000

    distances = np.array(sample.distances)
    indices = np.where(distances < 10000)

    distances = distances[indices]
    angles = np.array(sample.angles)[indices]

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

    for i in range(len(angles)):
        angle = angles[i]
        distance = distances[i]

        distance = distance * 0.1

        if distance > radius:
            continue

        x = center[0] + distance * np.cos(np.deg2rad(angle))
        y = center[1] + distance * np.sin(np.deg2rad(angle))

        cv2.circle(frame, (int(x), int(y)), 1, (0.0, 0.0, 1.0, 1.0), 2)

    # only keep values for angles between [0, 90] and [270, 360]
    indices = np.where(
        (angles >= 0) & (angles <= 90) | (angles >= 270) & (angles <= 360)
    )

    distances = distances[indices]
    angles = angles[indices]

    indices = np.where(distances < radius * 10)

    distances = distances[indices]
    angles = angles[indices]

    extended_distances = np.concatenate([distances[-5:], distances, distances[:5]])

    local_means = np.array(
        [np.mean(extended_distances[i : i + 2 * 5 + 1]) for i in range(len(distances))]
    )

    disc = np.where(np.abs(distances - local_means) > 500)

    new_angles = angles[disc]
    new_distances = distances[disc]

    for i in range(len(new_angles)):
        angle = new_angles[i]
        distance = new_distances[i]

        distance = distance * 0.1

        if distance > radius:
            continue

        x = center[0] + distance * np.cos(np.deg2rad(angle))
        y = center[1] + distance * np.sin(np.deg2rad(angle))

        cv2.circle(frame, (int(x), int(y)), 1, (1.0, 0.0, 0.0, 1.0), 2)

    angles_rad = np.deg2rad(new_angles)

    x = new_distances * np.cos(angles_rad)
    y = new_distances * np.sin(angles_rad)

    points = np.vstack((x, y)).T

    if len(points) >= 1:
        clusters = DBSCAN(eps=100, min_samples=1).fit(points)

        for i in range(len(np.unique(clusters.labels_))):
            indices = np.where(clusters.labels_ == i)

            cluster = points[indices]

            if len(cluster) < 2:
                continue

            x = np.mean(cluster[:, 0])
            y = np.mean(cluster[:, 1])

            cv2.circle(
                frame,
                (int(center[0] + x * 0.1), int(center[1] + y * 0.1)),
                5,
                (0.0, 1.0, 0.0, 1.0),
                2,
            )

        if len(np.unique(clusters.labels_)) >= 2:
            mean = np.mean(points, axis=0)

            cv2.circle(
                frame,
                (int(center[0] + mean[0] * 0.1), int(center[1] + mean[1] * 0.1)),
                5,
                (1.0, 1.0, 0.0, 1.0),
                2,
            )
            cv2.polylines(
                frame,
                [
                    np.array(
                        [
                            center,
                            (
                                int(center[0] + mean[0] * 0.1),
                                int(center[1] + mean[1] * 0.1),
                            ),
                        ]
                    )
                ],
                False,
                (1.0, 1.0, 0.0, 1.0),
                2,
            )

    """
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


    """
    try:
        dpg.set_value("visualizer", frame)
    except:
        print("ERROR")
