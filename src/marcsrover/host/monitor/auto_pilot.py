import zenoh

import dearpygui.dearpygui as dpg

from marcsrover.message import AutoPilot

def callback(session: zenoh.Session) -> None:
    bytes = AutoPilot(
        min_speed=dpg.get_value("min_speed"),
        max_speed=dpg.get_value("max_speed"),
        back_speed=dpg.get_value("back_speed"),
        steering=dpg.get_value("steering"),
        back_treshold=dpg.get_value("back_treshold"),
        fwd_treshold=dpg.get_value("fwd_treshold"),
        steering_treshold=dpg.get_value("steering_treshold"),
        steering_min_angle=dpg.get_value("steering_min_angle"),
        steering_max_angle=dpg.get_value("steering_max_angle"),
    ).serialize()

    session.put("marcsrover/autopilot/config", bytes)

def init_autopilot(session: zenoh.Session) -> None:
    with dpg.window(label="autopilot", width=256, height=256, pos=(1024, 128+256)):
        dpg.add_slider_int(
            label="min_speed",
            tag="min_speed",
            width=150,
            min_value=0,
            max_value=2000,
            default_value=0,
        )
        dpg.add_slider_int(
            label="max_speed",
            tag="max_speed",
            width=150,
            min_value=0,
            max_value=2000,
            default_value=0,
        )
        dpg.add_slider_int(
            label="back_speed",
            tag="back_speed",
            width=150,
            min_value=0,
            max_value=3000,
            default_value=0,
        )
        dpg.add_slider_int(
            label="steering",
            tag="steering",
            width=150,
            min_value=0,
            max_value=90,
            default_value=90,
        )
        dpg.add_slider_float(
            label="back_treshold",
            tag="back_treshold",
            width=150,
            min_value=0,
            max_value=2,
            default_value=0.5,
        )
        dpg.add_slider_float(
            label="fwd_treshold",
            tag="fwd_treshold",
            width=150,
            min_value=0,
            max_value=2,
            default_value=0.5,
        )
        dpg.add_slider_float(
            label="steering_treshold",
            tag="steering_treshold",
            width=150,
            min_value=0,
            max_value=2,
            default_value=0.5,
        )
        dpg.add_slider_int(
            label="steering_min_angle",
            tag="steering_min_angle",
            width=150,
            min_value=0,
            max_value=90,
            default_value=45,
        )
        dpg.add_slider_int(
            label="steering_max_angle",
            tag="steering_max_angle",
            width=150,
            min_value=0,
            max_value=90,
            default_value=90,
        )
        dpg.add_button(label="send", width=150, callback=lambda:callback(session))
