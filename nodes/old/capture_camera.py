import dataclasses
import zenoh
import cv2
import numpy as np

# We import the CameraFrame message from the message module
from message import CameraFrame

# We create a class to encapsulate the camera capture and zenoh setup
class CaptureCamera:
    def __init__(self, topic= "marcsrover/camera", path="/dev/video0", width=640, height=480):
        # Camera VideoCapture setup with OpenCV

        if isinstance(path, str) and path.isnumeric():
            path = int(path)

        self.video_capture = cv2.VideoCapture(path)
        self.width = width
        self.height = height

        # Zenoh setup

        config = zenoh.Config.from_file("zenoh_config.json")
        self.session = zenoh.open(config)

        self.camera_publisher = self.session.declare_publisher(topic)

    # The run method is where we capture the camera frames and publish them to Zenoh
    def run(self):
        while True:
            ret, frame = self.video_capture.read()

            if not ret:
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                cv2.putText(
                    frame,
                    f"Error: no frame for this camera.",
                    (int(30), int(30)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.50,
                    (255, 255, 255),
                    1,
                    1,
                )


            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])[1].tobytes()

            frame = CameraFrame(frame=frame, width=self.width, height=self.height)

            # Publish the frame to Zenoh, serialized as a CameraFrame message
            self.camera_publisher.put(CameraFrame.serialize(frame))

if __name__ == "__main__":
    capture_camera = CaptureCamera(path="/dev/video0", width=640, height=480)
    capture_camera.run()
