import PySimpleGUI as sg
from gui.scanner_gui import step0_layout


def step1_layout():
    step1_layout = [
        [sg.T('Corner 1', s=(11, 1)),

         sg.T('X:'),
         sg.I("", key="-S1CORNER1_X-", s=(10, 2)),

         sg.T("Y:"),
         sg.I("", key="-S1CORNER1_Y-", s=(10, 2)),

         sg.B("Read", key="-S1READ_COORD1-"),
         sg.B("Go here", key="-S1GOTOCORD1-")],

        [sg.T('Corner 2', s=(11, 1)),

         sg.T('X:'),
         sg.I("", key="-S1CORNER2_X-", s=(10, 2)),

         sg.T("Y:"),
         sg.I("", key="-S1CORNER2_Y-", s=(10, 2)),

         sg.B("Read", key="-S1READ_COORD2-"),
         sg.B("Go here", key="-S1GOTOCORD2-")],

        [sg.B("Save Coordinates", key="-STEP1SUBMIT-"),
         sg.B('Load Coordinates', key="-STEP1LOAD-")]
    ]

    step1 = sg.Frame(layout=step1_layout, title="Initial position")
    return step1


def step2_layout():
    step2_layout = [
        [sg.T('Corner 1', s=(11, 1)),

         sg.T('X:'),
         sg.I("", key="-S2CORNER1_X-", s=(10, 2)),

         sg.T("Y:"),
         sg.I("", key="-S2CORNER1_Y-", s=(10, 2)),

         sg.B("Read", key="-S2READ_COORD1-"),
         sg.B("Go here", key="-S2GOTOCORD1-")],

        [sg.T('Corner 2', s=(11, 1)),

         sg.T('X:'),
         sg.I("", key="-S2CORNER2_X-", s=(10, 2)),

         sg.T("Y:"),
         sg.I("", key="-S2CORNER2_Y-", s=(10, 2)),

         sg.B("Read", key="-S2READ_COORD2-"),
         sg.B("Go here", key="-S2GOTOCORD2-")],

        [sg.B("Convert points", key="-STEP2SUBMIT-"),
         sg.B("Same values", key="-SAMEVALUES-"),
         sg.B("TEST", key="-TEST-")]
    ]
    step2 = sg.Frame(layout=step2_layout, title="New position")
    return step2


class PositionGUI:
    def __init__(self):
        self.window = self.create_layout()

    def create_layout(self):
        # sg.theme("Reddit")
        window = sg.Window('New point calculator',
                           layout=[[step0_layout()], [step1_layout()],
                                   [step2_layout()]],
                           finalize=True,
                           font='"Verdana" 12')
        return window


if __name__ == "__main__":
    gui = PositionGUI()
    window = gui.window
    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
