import PySimpleGUI as sg


def create_layout():
    layout = [
        [sg.B("Add point", key="-ADDPOINTOFINT-"), sg.B("Remove last point", key="-REMOVELAST-")],
        [sg.T("Current point count:"), sg.T("0", key="-CURRENTPOINTCOUNT-")],
        [
            sg.T("Number of scans per two points: "),
            sg.I("", key="-NUMBER_OF_SCANS-", s=(9, 2), enable_events=1, justification="c"),
            sg.B("Submit", key="-SUMBMISCANNO-"),
        ],
        [sg.T("Total scanning point count:"), sg.T("0", key="-POINTCOUNT-")],
        [sg.B("Save points", key="-SAVESCANPOINTS-")],
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
