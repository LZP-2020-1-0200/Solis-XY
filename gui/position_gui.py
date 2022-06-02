import PySimpleGUI as sg
from gui.helpers import disable_element

CORNER_COUNT = 2


def disable_step_elements(window: sg.Window, step: int):

    for i in range(1, CORNER_COUNT + 1):
        disable_element(window, f"-S{step}CORNER{i}_X-")
        disable_element(window, f"-S{step}CORNER{i}_Y-")
        disable_element(window, f"-S{step}READ_COORD{i}-")
    disable_element(window, f"-STEP{step}SUBMIT-")

    if step == 1:
        disable_element(window, f"-STEP{step}LOAD-")
    else:
        disable_element(window, "-SAMEVALUES-")


def step1_layout():
    layout = []
    for i in range(1, CORNER_COUNT + 1):
        input_row = [
            sg.T(f"Corner {i}", s=(11, 1)),
            sg.T("X:"),
            sg.I("", key=f"-S1CORNER{i}_X-", s=(10, 2)),
            sg.T("Y:"),
            sg.I("", key=f"-S1CORNER{i}_Y-", s=(10, 2)),
            sg.B("Read", key=f"-S1READ_COORD{i}-"),
            sg.B("Go here", key=f"-S1GOTOCORD{i}-"),
        ]
        layout.append(input_row)

    save_layout = [sg.B("Save Coordinates", key="-STEP1SUBMIT-"), sg.B("Load Coordinates", key="-STEP1LOAD-")]

    layout.append(save_layout)

    step1 = sg.Frame(layout=layout, title="Initial position")
    return step1


def step2_layout():
    layout = []
    for i in range(1, CORNER_COUNT + 1):
        input_row = [
            sg.T(f"Corner {i}", s=(11, 1)),
            sg.T("X:"),
            sg.I("", key=f"-S2CORNER{i}_X-", s=(10, 2)),
            sg.T("Y:"),
            sg.I("", key=f"-S2CORNER{i}_Y-", s=(10, 2)),
            sg.B("Read", key=f"-S2READ_COORD{i}-"),
            sg.B("Go here", key=f"-S2GOTOCORD{i}-"),
        ]
        layout.append(input_row)

    save_layout = [
        sg.B("Save Coordinates", key="-STEP2SUBMIT-"),
        sg.B("Convert points", key="-CONVERTPOINTS-"),
        sg.B("Fill with same values", key="-SAMEVALUES-"),
    ]

    layout.append(save_layout)
    step2 = sg.Frame(layout=layout, title="New position")
    return step2


class PositionGUI:
    def __init__(self):
        self.window = self.create_layout()

    def create_layout(self):
        # sg.theme("Reddit")
        window = sg.Window(
            "New point calculator",
            layout=[[step1_layout()], [step2_layout()]],
            finalize=True,
            font='"Verdana" 12',
        )
        return window


if __name__ == "__main__":
    gui = PositionGUI()
    window = gui.window
    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
