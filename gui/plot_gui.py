import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from matplotlib.patches import Rectangle
from matplotlib import pyplot as plt

sg.theme('Reddit')


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


class PlotGUI():
    def __init__(self):
        self.window = sg.Window('Visualization', [[sg.Canvas(key='-CANVAS-')]], finalize=True,
                                element_justification='center',
                                font='Helvetica 14')
        self.fig, self.ax = plt.subplots(figsize=(5, 5), dpi=100)
        # self.random_point = self.ax.plot([],[])
        self.fig_agg = draw_figure(self.window['-CANVAS-'].TKCanvas, self.fig)
        self.ax.axis('equal')

# fig = matplotlib.figure.Figure(figsize=(5, 5), dpi=100)
# ax1 = fig.add_subplot(111)

# ax1.axis('equal')
# ax1.add_patch(Rectangle((0,0),30,20))
# ax1.scatter([29,28,27,26],[10,10,10,10],color="orange",s=2)

# plot_gui = Plot_GUI()

# while 1:
#     event, values = plot_gui.window.read()
#     if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
#         break
