import zenoh

import dearpygui.dearpygui as dpg

from marcsrover.message import IMU


def imu_callback(sample: zenoh.Sample) -> None:
    motor = IMU.deserialize(sample.payload.to_bytes())

    try:
        dpg.set_value("Accel X", motor.accel_x)
        dpg.set_value("Accel Y", motor.accel_y)
        dpg.set_value("Accel Z", motor.accel_z)
        dpg.set_value("Gyro X", motor.gyro_x)
        dpg.set_value("Gyro Y", motor.gyro_y)
        dpg.set_value("Gyro Z", motor.gyro_z)
    except:
        print("error while setting IMU values to dearpygui")


def init_imu(session: zenoh.Session) -> None:
    _ = session.declare_subscriber("marcsrover/imu", imu_callback)

    with dpg.window(label="IMU", width=256, height=256, pos=(1024, 128)):
        dpg.add_slider_float(
            label="Accel X",
            tag="Accel X",
            width=150,
            min_value=-10,
            max_value=10,
            default_value=0,
        )
        dpg.add_slider_float(
            label="Accel Y",
            tag="Accel Y",
            width=150,
            min_value=-10,
            max_value=10,
            default_value=0,
        )
        dpg.add_slider_float(
            label="Accel Z",
            tag="Accel Z",
            width=150,
            min_value=-10,
            max_value=10,
            default_value=0,
        )
        dpg.add_slider_float(
            label="Gyro X",
            tag="Gyro X",
            width=150,
            min_value=-10,
            max_value=10,
            default_value=0,
        )
        dpg.add_slider_float(
            label="Gyro Y",
            tag="Gyro Y",
            width=150,
            min_value=-10,
            max_value=10,
            default_value=0,
        )
        dpg.add_slider_float(
            label="Gyro Z",
            tag="Gyro Z",
            width=150,
            min_value=-10,
            max_value=10,
            default_value=0,
        )
