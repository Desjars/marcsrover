import zenoh

import dearpygui.dearpygui as dpg

from marcsrover.message import RoverControl


def control_callback(sample: zenoh.Sample) -> None:
    motor = RoverControl.deserialize(sample.payload.to_bytes())

    try:
        dpg.set_value("Steering", motor.steering)
        dpg.set_value("Speed", motor.speed)
    except:
        print("error while setting controller values to dearpygui")


def init_controller(session: zenoh.Session) -> None:
    _ = session.declare_subscriber("marcsrover/control", control_callback)

    with dpg.window(label="Controller", width=256, height=128, pos=(1024, 0)):
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
