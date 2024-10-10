import argparse
import os
import time

import dearpygui.dearpygui as dpg

import cv2
import numpy as np
import pyarrow as pa

import zenoh


image_width = 640
image_height = 480

def main():
    config = zenoh.Config.from_file("zenoh_config.json")
    session = zenoh.open(config)

    dpg.create_context()
    dpg.create_viewport(title='MarcsRover', width=640, height=480)
    dpg.setup_dearpygui()

    texture_data = np.zeros((image_width, image_height, 3), dtype=np.float32)

    def camera_callback(sample):
        image = np.frombuffer(bytes(sample.value.payload), dtype=np.uint8)
        image = cv2.imdecode(image, 1)

        data = np.flip(image, 2)  # because the camera data comes in as BGR and we need RGB
        data = data.ravel()  # flatten camera data to a 1 d stricture
        data = np.asarray(data, dtype='f')  # change data type to 32bit floats

        texture_data = np.true_divide(data, 255.0)  # normalize image data to prepare for GPU
        dpg.set_value("texture_tag", texture_data)


    camera_subscriber = session.declare_subscriber("marcsrover/camera", camera_callback)

    with dpg.texture_registry(show=True):
        dpg.add_raw_texture(image_width, image_height, texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb)

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello, world")
        dpg.add_image("texture_tag")

    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
