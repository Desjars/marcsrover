from typing import List

class Lidar:
    def __init__(self, name: str) -> None:
        pass

    def enable(self, sensor_time_step: int) -> None:
        pass

    def enablePointCloud(self) -> None:
        pass

    def getRangeImage(self) -> List[float]:
        pass

class Camera:
    def __init__(self, name: str) -> None:
        pass

    def enable(self, sensor_time_step: int) -> None:
        pass

    def getImage(self) -> bytes:
        pass

class RangeFinder:
    def __init__(self, name: str) -> None:
        pass

    def enable(self, sensor_time_step: int) -> None:
        pass
