import PySimpleGUI as sg
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
from matplotlib.patches import Rectangle

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def convertStringToNum(args: list[float]) -> list[float]:
    return [float(arg) for arg in args]


def numericCheck(list: list[str]):
    try:
        for string in list:
            float(string)
    except ValueError:
        return False
    return True

fig = matplotlib.figure.Figure(figsize=(3, 2), dpi=75)
ax1 = fig.add_subplot(111)


sg.theme('Reddit')

layout = [
    [sg.T('1. Corner'), sg.I("", key="CORNER1", s=(10, 2)), sg.T('3. Corner'), sg.I("", key="CORNER3", s=(10, 2))],
    [sg.T('2. Corner'), sg.I("", key="CORNER2", s=(10, 2)), sg.T('4. Corner'), sg.I("", key="CORNER4", s=(10, 2))],
    [sg.B("Submit", key="STEP1SUBMIT"), sg.B('Load', key="STEP1LOAD")]]



step1 = sg.Frame(layout=layout, title="Step 1 - Initial position")


layout = [
    [sg.T('1. Corner'), sg.I("", key="CORNER1", s=(10, 2)), sg.T('3. Corner'), sg.I("", key="CORNER3", s=(10, 2))],
    [sg.T('2. Corner'), sg.I("", key="CORNER2", s=(10, 2)), sg.T('4. Corner'), sg.I("", key="CORNER4", s=(10, 2))],
    [sg.B("Submit", key="STEP1SUBMIT"), sg.B('Load', key="STEP1LOAD")]]

step2 = sg.Frame(layout=layout, title="Step 2 - New position")

window = sg.Window('Test', [[step1,  sg.Canvas(key='-CANVAS-')], [step2]], finalize=True, element_justification='center',
                   font='Helvetica 14')

while 1:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break

    if event == "STEP1SUBMIT":
        initial_values = [values[f"CORNER{str(i)}"] for i in range(1, 5)]
        if not numericCheck(initial_values):
            continue
        
        ax1.plot([], [])
        ax1.add_patch(Rectangle(0,0))
        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)






