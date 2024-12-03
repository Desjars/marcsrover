import zenoh

import dearpygui.dearpygui as dpg
import threading

callback_to_call = "cartographer"
mutex = threading.Lock()


def cartographer_callback(sample: zenoh.Sample) -> None:
    mutex.acquire()
    callback = callback_to_call
    mutex.release()

    if callback != "cartographer":
        return


def realsense_callback(sample: zenoh.Sample) -> None:
    mutex.acquire()
    callback = callback_to_call
    mutex.release()

    if callback != "realsense":
        return


def lidar_callback(sample: zenoh.Sample) -> None:
    mutex.acquire()
    callback = callback_to_call
    mutex.release()

    if callback != "lidar":
        return


def opencv_camera_callback(sample: zenoh.Sample) -> None:
    mutex.acquire()
    callback = callback_to_call
    mutex.release()

    if callback != "opencv":
        return


def set_callback_to_call(callback: str) -> None:
    global mutex, callback_to_call

    mutex.acquire()
    callback_to_call = callback
    mutex.release()


def init_main_window(session: zenoh.Session) -> None:
    _ = session.declare_subscriber("marcsrover/realsense", realsense_callback)
    _ = session.declare_subscriber("marcsrover/lidar", lidar_callback)
    _ = session.declare_subscriber("marcsrover/opencv-camera", opencv_camera_callback)

    with dpg.window(label="Visualizer", width=1024, height=720, pos=(0, 0)):
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
