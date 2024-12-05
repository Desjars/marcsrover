import numpy as np


def z16_to_XY8(depth_image) -> np.ndarray:
    width = depth_image.shape[1]
    height = depth_image.shape[0]

    u8_depth = np.zeros((height, width, 2), dtype=np.uint8)

    # low byte
    u8_depth[:, :, 0] = (depth_image & 0xFF).astype(np.uint8)
    # high byte
    u8_depth[:, :, 1] = ((depth_image >> 8) & 0xFF).astype(np.uint8)

    return u8_depth


def XY8_to_z16(depth_image) -> np.ndarray:
    width = depth_image.shape[1]
    height = depth_image.shape[0]

    z16_depth = np.zeros((height, width), dtype=np.uint16)
    z16_depth = ((depth_image[:, :, 1].astype(np.uint16) << 8) | depth_image[:, :, 0].astype(np.uint16))

    return z16_depth

def XY8_to_BGR8(depth_image) -> np.ndarray:
    width = depth_image.shape[1]
    height = depth_image.shape[0]

    z16 = XY8_to_z16(depth_image)

    max_value = 15.0 * 1000.0
    # max_value = 2**16 - 1

    z16 = np.asarray(z16, dtype=np.float32)
    z16 = np.true_divide(z16, max_value)
    z8 = (z16 * 255).astype(np.uint8)

    bgr8 = np.zeros((height, width, 3), dtype=np.uint8)
    bgr8[:, :, 0] = z8
    bgr8[:, :, 1] = z8
    bgr8[:, :, 2] = z8

    return bgr8
