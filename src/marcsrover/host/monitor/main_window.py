import zenoh
import threading
import cv2
import numpy as np

import dearpygui.dearpygui as dpg

from marcsrover.host.monitor.auto_pilot import draw_auto_pilot
from marcsrover.message import LidarScan

frame_name = "auto_pilot"
mutex = threading.Lock()


def lidar_callback(sample: zenoh.Sample) -> None:
    global frame, mutex_frame

    if frame_name != "auto_pilot":
        return

    draw_auto_pilot(LidarScan.deserialize(sample.payload.to_bytes()))


def slam_callback(sample: zenoh.Sample) -> None:
    if frame_name != "slam":
        return


def change_frame(name: str) -> None:
    global mutex, frame_name
    with mutex:
        frame_name = name


def init_main_window(session: zenoh.Session) -> None:
    _ = session.declare_subscriber("marcsrover/lidar", lidar_callback)

    with dpg.texture_registry():
        dpg.add_raw_texture(
            1024, 720, [], tag="visualizer", format=dpg.mvFormat_Float_rgba
        )

    with dpg.window(label="Visualizer", width=1024, height=720, pos=(0, 0)):
        dpg.add_image("visualizer", pos=(0, 0))

        with dpg.menu_bar():
            dpg.add_button(
                label="Auto Pilot", callback=lambda: change_frame("auto_pilot")
            )
            dpg.add_button(label="SLAM", callback=lambda: change_frame("slam"))
