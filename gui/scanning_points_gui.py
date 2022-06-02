import PySimpleGUI as sg


def create_layout():
    layout = [
        [sg.B("Add point", key="-ADDPOINTOFINT-"), sg.B("Remove last point", key="-REMOVELAST-")],
        [sg.T("Current point count:"), sg.T("0", key="-CURRENTPOINTCOUNT-")],
        [
            sg.B("Add height point", key="-GETHEIGHT-"),
            sg.T("0 μm", key="-HEIGHT-"),
        ],
        [
            sg.T("Number of scans: ", s=(14, 1)),
            sg.I("", key="-NUMBER_OF_SCANS-", s=(7, 2), enable_events=1, justification="c"),
        ],
        [sg.T("Number of lines:", s=(14, 1)), sg.I("1", key="-NUMOFLINES-", s=(7, 2), justification="c")],
        [sg.B("Calculate points", key="-SUMBMISCANNO-"), sg.B("Save points", key="-SAVESCANPOINTS-")],
    ]

    layout = sg.Frame(layout=layout, title="", expand_x=True)
    return layout


class ScannerPointsGUI:
    def __init__(self):
        self.window = self.create_layout()

    def create_layout(self):
        # sg.theme("Reddit")
        window = sg.Window(
            "Scanning points",
            layout=[[create_layout()]],
            finalize=True,
            font='"Verdana" 12',
            return_keyboard_events=True,
        )

        return window


if __name__ == "__main__":
    gui = ScannerPointsGUI()
    window = gui.window
    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
