import zenoh

import dearpygui.dearpygui as dpg
import threading

from marcsrover.host.monitor.cartographer import cartographer_draw
from marcsrover.host.monitor.realsense import realsense_draw
from marcsrover.host.monitor.lidar import lidar_draw
from marcsrover.host.monitor.opencv import opencv_draw
from marcsrover.message import D435I, SLAM, LidarScan, BytesMessage

callback_to_call = "lidar"
mutex = threading.Lock()


def cartographer_callback(sample: zenoh.Sample) -> None:
    mutex.acquire()
    callback = callback_to_call
    mutex.release()

    if callback != "cartographer":
        return

    cartographer_draw(SLAM.deserialize(sample.payload.to_bytes()))


def realsense_callback(sample: zenoh.Sample) -> None:
    mutex.acquire()
    callback = callback_to_call
    mutex.release()

    if callback != "realsense":
        return

    realsense_draw(D435I.deserialize(sample.payload.to_bytes()))


def lidar_callback(sample: zenoh.Sample) -> None:
    mutex.acquire()
    callback = callback_to_call
    mutex.release()

    if callback != "lidar":
        return

    lidar_draw(LidarScan.deserialize(sample.payload.to_bytes()))


def opencv_camera_callback(sample: zenoh.Sample) -> None:
    mutex.acquire()
    callback = callback_to_call
    mutex.release()

    if callback != "opencv":
        return

    opencv_draw(BytesMessage.deserialize(sample.payload.to_bytes()))


def set_callback_to_call(callback: str) -> None:
    global mutex, callback_to_call

    mutex.acquire()
    callback_to_call = callback
    mutex.release()


def init_main_window(session: zenoh.Session) -> None:
    _ = session.declare_subscriber("marcsrover/realsense", realsense_callback)
    _ = session.declare_subscriber("marcsrover/lidar", lidar_callback)
    _ = session.declare_subscriber("marcsrover/opencv-camera", opencv_camera_callback)

    with dpg.texture_registry():
        dpg.add_raw_texture(
            1024, 720, [], tag="visualizer", format=dpg.mvFormat_Float_rgba
        )

    with dpg.window(label="Visualizer", width=1024, height=720, pos=(0, 0)):
        dpg.add_image("visualizer", pos=(0, 0))

        with dpg.menu_bar():
            dpg.add_button(
                label="Cartographer",
                callback=lambda: set_callback_to_call("cartographer"),
            )
            dpg.add_button(
                label="Realsense", callback=lambda: set_callback_to_call("realsense")
            )
            dpg.add_button(
                label="OpenCV", callback=lambda: set_callback_to_call("opencv")
            )
            dpg.add_button(
                label="LiDAR", callback=lambda: set_callback_to_call("lidar")
            )
