import zenoh
import json
import cv2

import numpy as np
import dearpygui.dearpygui as dpg

from marcsrover.message import D435I, LidarScan, OpenCVCamera, RoverControl


class Node:
    def __init__(self):
        self.zenoh_config: zenoh.Config = zenoh.Config.from_json5("{}")

        self.zenoh_config.insert_json5(
            "connect/endpoints", json.dumps(["udp/127.0.0.1:7447"])
        )
        self.zenoh_config.insert_json5(
            "listen/endpoints", json.dumps(["udp/0.0.0.0:0"])
        )
        self.zenoh_config.insert_json5("scouting/multicast/enabled", json.dumps(False))
        self.zenoh_config.insert_json5("scouting/gossip/enabled", json.dumps(True))

        dpg.create_context()
        dpg.create_viewport(
            title="MARCSRover",
            width=1280,
            height=960,
            x_pos=1920 // 2 - 1280 // 2,
            y_pos=1280 // 2 - 960 // 2,
        )
        dpg.setup_dearpygui()

    def run(self) -> None:
        with zenoh.open(self.zenoh_config) as session:
            realsense = session.declare_subscriber(
                "marcsrover/realsense", self.realsense_callback
            )

            lidar = session.declare_subscriber("marcsrover/lidar", self.lidar_callback)
            control = session.declare_subscriber(
                "marcsrover/control", self.control_callback
            )

            camera = session.declare_subscriber(
                "marcsrover/opencv-camera", self.opencv_camera_callback
            )

            dpg.show_viewport()

            with dpg.texture_registry():
                dpg.add_raw_texture(
                    640, 480, [], tag="realsense-rgb", format=dpg.mvFormat_Float_rgb
                )
                dpg.add_raw_texture(
                    640, 480, [], tag="realsense-depth", format=dpg.mvFormat_Float_rgb
                )

            with dpg.window(
                label="Realsense Camera", width=1280, height=480, pos=(0, 0)
            ):
                dpg.add_image("realsense-rgb", pos=(0, 0))
                dpg.add_image("realsense-depth", pos=(640, 0))

            with dpg.window(
                label="LiDAR", tag="LiDAR", width=640, height=480, pos=(0, 480)
            ):
                dpg.add_slider_float(
                    label="LiDAR Scale",
                    tag="LiDAR Scale",
                    width=150,
                    min_value=1,
                    max_value=200,
                    default_value=100,
                )

                with dpg.drawlist(width=640, height=480) as self.lidar_canvas:
                    pass

            with dpg.window(label="Controller", width=640, height=480, pos=(640, 480)):
                dpg.add_slider_float(
                    label="Speed",
                    tag="Speed",
                    width=150,
                    min_value=-4000,
                    max_value=4000,
                    default_value=0,
                )
                dpg.add_slider_float(
                    label="Steering",
                    tag="Steering",
                    width=150,
                    min_value=-90,
                    max_value=90,
                    default_value=0,
                )

            try:
                while dpg.is_dearpygui_running():
                    dpg.render_dearpygui_frame()
            except KeyboardInterrupt:
                print("Monitor received KeyboardInterrupt")

            dpg.destroy_context()

            lidar.undeclare()
            control.undeclare()
            realsense.undeclare()
            camera.undeclare()

            session.close()

        print("Monitor stopped")

    def opencv_camera_callback(self, sample: zenoh.Sample) -> None:
        image: OpenCVCamera = OpenCVCamera.deserialize(sample.payload.to_bytes())
        rgb = np.frombuffer(bytes(image.frame), dtype=np.uint8)
        rgb = cv2.imdecode(rgb, cv2.IMREAD_COLOR)

        data = np.flip(rgb, 2)
        data = data.ravel()
        data = np.asarray(data, dtype="f")

        texture_data = np.true_divide(data, 255.0)
        try:
            dpg.set_value("realsense-rgb", texture_data)
        except:
            print("ERROR")

    def realsense_callback(self, sample: zenoh.Sample) -> None:
        realsense: D435I = D435I.deserialize(sample.payload.to_bytes())
        rgb = np.frombuffer(bytes(realsense.rgb), dtype=np.uint8)
        rgb = cv2.imdecode(rgb, cv2.IMREAD_COLOR)
        depth = np.frombuffer(bytes(realsense.depth), dtype=np.uint8)
        depth = cv2.imdecode(depth, cv2.IMREAD_COLOR)

        data = np.flip(rgb, 2)
        data = data.ravel()
        data = np.asarray(data, dtype="f")

        texture_data = np.true_divide(data, 255.0)

        try:
            print(texture_data.shape)
            # dpg.set_value("realsense-rgb", texture_data)
        except:
            print("ERROR")

        data = np.flip(depth, 2)
        data = data.ravel()
        data = np.asarray(data, dtype="f")

        texture_data = np.true_divide(data, 255.0)

        try:
            print(texture_data.shape)
            # dpg.set_value("realsense-depth", texture_data)
        except:
            print("ERROR")

    def lidar_callback(self, sample):
        lidar_scale = dpg.get_value("LiDAR Scale")

        lidar = LidarScan.deserialize(sample.payload.to_bytes())

        try:
            dpg.delete_item(self.lidar_canvas)
            with dpg.drawlist(
                width=640, height=480, parent="LiDAR"
            ) as self.lidar_canvas:
                radius = 190

                dpg.draw_circle(
                    center=(320, 230),
                    radius=radius,
                    color=(255, 255, 255, 255),
                    thickness=1,
                )
                dpg.draw_circle(
                    center=(320, 230), radius=5, color=(255, 0, 0, 255), thickness=5
                )

                for i in range(0, 360, 30):
                    x = 320 + radius * np.cos(np.radians(i))
                    y = 230 + radius * np.sin(np.radians(i))
                    dpg.draw_line(
                        (320, 230), (x, y), color=(255, 255, 255, 255), thickness=1
                    )

                    text_x = 320 + (radius + 20) * np.cos(np.radians(i)) - i * 20 / 360
                    text_y = 230 + (radius + 20) * np.sin(np.radians(i)) - i * 20 / 360

                    dpg.draw_text(
                        (text_x, text_y), str(i), color=(255, 255, 255, 255), size=16
                    )

                for i in range(len(lidar.angles)):
                    angle = lidar.angles[i]
                    distance = lidar.distances[i]

                    x = 320 + distance * np.cos(np.radians(angle)) * lidar_scale / 200
                    y = 230 + distance * np.sin(np.radians(angle)) * lidar_scale / 200

                    if np.sqrt((x - 320) ** 2 + (y - 230) ** 2) > radius:
                        continue

                    dpg.draw_circle(
                        (int(x), int(y)), 1, color=(0, 0, 255, 255), thickness=5
                    )
        except:
            print("ERROR")

    def control_callback(self, sample):
        motor = RoverControl.deserialize(sample.payload.to_bytes())

        try:
            dpg.set_value("Steering", motor.steering)
            dpg.set_value("Speed", motor.speed)
        except:
            print("ERROR")


node = Node()
node.run()
