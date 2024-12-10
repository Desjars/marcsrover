import zenoh

import dearpygui.dearpygui as dpg


def init_main_window(session: zenoh.Session) -> None:
    with dpg.texture_registry():
        dpg.add_raw_texture(
            1024, 720, [], tag="visualizer", format=dpg.mvFormat_Float_rgba
        )

    with dpg.window(label="Visualizer", width=1024, height=720, pos=(0, 0)):
        dpg.add_image("visualizer", pos=(0, 0))

        with dpg.menu_bar():
            dpg.add_button(label="Auto Pilot")
            dpg.add_button(label="SLAM")
