import PySimpleGUI as sg


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
        [sg.B("Go to First Point", key="-GOFIRSTPOINT-")],
        [sg.T("Scans per point: "), sg.I("1", s=(3, 1), justification="c", key="-NUMOFSCANS-")],
        [sg.T("Total integration time (Seconds): "), sg.I("10", key="-INTEGRATIONTIME-", s=(5, 2), justification="c")],
        [
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
            layout=[[step3_layout()]],
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
