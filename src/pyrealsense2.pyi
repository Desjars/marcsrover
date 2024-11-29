class Stream:
    depth = 0
    color = 1
    accel = 2
    gyro = 3

stream = Stream()

class Format:
    z16 = 0
    bgr8 = 1

format = Format()

class Config:
    def enable_stream(
        self,
        stream: int,
        width: int = 0,
        height: int = 0,
        format: int = 0,
        rate: int = 0,
    ):
        pass

class Pipeline:
    def start(self, config: Config):
        pass

    def wait_for_frames(self):
        pass

    def stop(self):
        pass

def pipeline() -> Pipeline:
    pass

def config() -> Config:
    pass
