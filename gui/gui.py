import PySimpleGUI as sg
from gui.buttons import get_available_com_ports


def step0_layout():
    step_0_layout = [[sg.T("COM Port: "), sg.Combo([*get_available_com_ports()], key="-COM_PORT_CHOOSER-", readonly=True),
                      sg.B("Refresh", key="-REFRESHCOMPORTS-"), sg.B("Connect", key="-CONNECT-")]]
    step0 = sg.Frame(layout=step_0_layout, title="Step 0 - COM Port chooser")
    return step0


def step1_layout():
    step1_layout = [
        [sg.T('Left btm corner', s=(14, 1)), sg.T('X:'), sg.I("-9999", key="-S1CORNER1_X-", s=(10, 2)), sg.T("Y:"),
         sg.I("-9001", key="-S1CORNER1_Y-", s=(10, 2)), sg.B("Read", key="-S1READ_COORD1"),sg.B("Go Here",key="-S1GOTOCOORD1-")],
        [sg.T('Left top corner', s=(14, 1)), sg.T('X:'), sg.I("-10001", key="-S1CORNER2_X-", s=(10, 2)), sg.T("Y:"),
         sg.I("8999", key="-S1CORNER2_Y-", s=(10, 2)), sg.B("Read", key="-S1READ_COORD2"),sg.B("Go Here",key="-S1GOTOCOORD2-")],
        [sg.T('Right top corner', s=(14, 1)), sg.T('X:'), sg.I("9999", key="-S1CORNER3_X-", s=(10, 2)), sg.T("Y:"),
         sg.I("9001", key="-S1CORNER3_Y-", s=(10, 2)), sg.B("Read", key="-S1READ_COORD3"),sg.B("Go Here",key="-S1GOTOCOORD3-")],
        [sg.T('Right btm corner', s=(14, 1)), sg.T('X:'), sg.I("10001", key="-S1CORNER4_X-", s=(10, 2)), sg.T("Y:"),
         sg.I("-8999", key="-S1CORNER4_Y-", s=(10, 2)), sg.B("Read", key="-S1READ_COORD4"),sg.B("Go Here",key="-S1GOTOCOORD4-")],
        [sg.B("Submit and Save", key="-STEP1SUBMIT-"), sg.B('Load', key="-STEP1LOAD-")]]

    step1 = sg.Frame(layout=step1_layout, title="Step 1 - Initial position")
    return step1


def step2_layout():
    step2_layout = [
        [sg.T('Left btm corner', s=(14, 1)), sg.T('X:'), sg.I("-9255", key="-S2CORNER1_X-", s=(10, 2)), sg.T("Y:"),
         sg.I("-9765", key="-S2CORNER1_Y-", s=(10, 2)), sg.B("Read", key="-S2READ_COORD1")],
        [sg.T('Left top corner', s=(14, 1)), sg.T('X:'), sg.I("-10682", key="-S2CORNER2_X-", s=(10, 2)), sg.T("Y:"),
         sg.I("8179", key="-S2CORNER2_Y-", s=(10, 2)), sg.B("Read", key="-S2READ_COORD2")],
        [sg.T('Right top corner', s=(14, 1)), sg.T('X:'), sg.I("9255", key="-S2CORNER3_X-", s=(10, 2)), sg.T("Y:"),
         sg.I("9765", key="-S2CORNER3_Y-", s=(10, 2)), sg.B("Read", key="-S2READ_COORD3")],
        [sg.T('Right btm corner', s=(14, 1)), sg.T('X:'), sg.I("10682", key="-S2CORNER4_X-", s=(10, 2)), sg.T("Y:"),
         sg.I("-8179", key="-S2CORNER4_Y-", s=(10, 2)), sg.B("Read", key="-S2READ_COORD4")],
        [sg.B("Submit", key="-STEP2SUBMIT-")]]
    step2 = sg.Frame(layout=step2_layout, title="Step 2 - New position")
    return step2


def step3_layout():
    step3_layout = [[sg.T("Number of scans: "), sg.I("", key="-NUMBER_OF_SCANS-", s=(20, 2), enable_events=1),
                     sg.B("Submit", key="-SUMBMISCANNO-")],
                    [sg.T("Current scan no.:"), sg.T("", key="-SCANNO-"),
                     sg.T("Current coordinates:", key="-CURRENTXY-")],
                    [sg.B("Previous", key="-PREVIOUS-"), sg.B("Next", key="-NEXT-")]]
    step3 = sg.Frame(layout=step3_layout, title="Step 3 - Scanning", expand_x=True)
    return step3


class GUI:
    def __init__(self):
        self.window = self.create_layout()

    def create_layout(self):
        sg.theme("Reddit")
        return sg.Window('Solis-XY',
                         [[step0_layout()], [step1_layout()], [step2_layout()], [step3_layout()], [sg.Canvas()]],
                         finalize=True, font='"Verdana" 12')
