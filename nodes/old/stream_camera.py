import zenoh
import cv2
import numpy as np

import dearpygui.dearpygui as dpg

# We import the CameraFrame message from the message module
from message import D435I

# We create a class to encapsulate the camera stream, dearpygui and zenoh setup
class StreamCamera:
    def __init__(self, topic= "marcsrover/camera", width=640, height=480):

        # DearPyGui setup
        dpg.create_context()
        dpg.create_viewport(title='MarcsRover', width=640, height=480)
        dpg.setup_dearpygui()

        self.width = width
        self.height = height

        # Zenoh setup

        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        self.camera_subscriber = self.session.declare_subscriber(topic, self.camera_callback)

    # The camera_callback method is where we receive the camera frames from Zenoh
    def camera_callback(self, sample):
        frame = D435I.deserialize(sample.value.payload)
        image = np.frombuffer(bytes(frame.frame), dtype=np.uint8)
        image = cv2.imdecode(image, 1)

        data = np.flip(image, 2)  # because the camera data comes in as BGR and we need RGB
        data = data.ravel()  # flatten camera data to a 1 d stricture
        data = np.asarray(data, dtype='f')  # change data type to 32bit floats

        texture_data = np.true_divide(data, 255.0)  # normalize image data to prepare for GPU
        dpg.set_value("texture", texture_data)

    # The run method is where we run the dearpygui loop
    def run (self):
        with dpg.texture_registry(show=True):
            dpg.add_raw_texture(self.width, self.height, [], tag="texture", format=dpg.mvFormat_Float_rgb)

        with dpg.window(label="Capture camera"):
            dpg.add_image("texture")

        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

if __name__ == "__main__":
    stream_camera = StreamCamera(topic="marcsrover/camera", width=640, height=480)
    stream_camera.run()
