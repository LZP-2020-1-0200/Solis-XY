import PySimpleGUI as sg
from gui.buttons import get_available_com_ports


def step0_layout():
    step_0_layout = [
        [
            sg.T("COM Port: "),
            sg.Combo([*get_available_com_ports()], key="-COM_PORT_CHOOSER-", readonly=True),
            sg.B("Refresh", key="-REFRESHCOMPORTS-"),
            sg.B("Connect", key="-CONNECT-"),
        ]
    ]
    step0 = sg.Frame(layout=step_0_layout, title="COM Port", expand_x=1)
    return step0


def step3_layout():
    step3_layout = [
        [sg.B("Add point", key="-ADDPOINTOFINT-"), sg.B("Remove last point", key="-REMOVELAST-")],
        [sg.T("Current point count:"), sg.T("0", key="-CURRENTPOINTCOUNT-")],
        [
            sg.T("Number of scans per two points: "),
            sg.I("", key="-NUMBER_OF_SCANS-", s=(9, 2), enable_events=1, justification="c"),
            sg.B("Submit", key="-SUMBMISCANNO-"),
        ],
        [sg.T("Total scanning point count:"), sg.T("0", key="-POINTCOUNT-")],
        [sg.B("Save points", key="-SAVESCANPOINTS-"), sg.B("Load points", key="-LOADSCANPOINTS-")],
        [
            sg.T("Scans per point: "),
            sg.I("1", s=(3, 1), justification="c", key="-NUMOFSCANS-"),
            sg.B("Start Scanning", key="-STARTSCAN-"),
        ],
    ]

    step3 = sg.Frame(layout=step3_layout, title="Scanner", expand_x=True)
    return step3


class AutomatizationGUI:
    def __init__(self):
        self.window = self.create_layout()

    def create_layout(self):
        # sg.theme("Reddit")
        window = sg.Window(
            "Auto-Scanner",
            layout=[[step0_layout()], [step3_layout()]],
            finalize=True,
            font='"Verdana" 12',
            return_keyboard_events=True,
        )

        return window


if __name__ == "__main__":
    gui = AutomatizationGUI()
    window = gui.window
    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
