import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt

sg.theme('Reddit')


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    figure_canvas_agg = FigureCanvasTkAgg(fig, canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)
        
def set_visible(patch, value,draw):
    patch.set_visible(value)  
    draw() 
        

def create_layout():
    
    canvas_layout = [sg.Canvas(key='-CANVAS-')],[sg.Canvas(key='-CONTROLS_CV-')]
    layout = [
        canvas_layout,
        [sg.Checkbox("Show first",key="-SHOW_FIRST-",default=True, enable_events=True), sg.Checkbox("Show second",key="-SHOW_SECOND-",default=True, enable_events=True),
         sg.Checkbox("Show points",key="-SHOW_POINTS-",default=True, enable_events=True), sg.Checkbox("Show current",key="-SHOW_CURRENT-",default=True, enable_events=True)]
        ]
    return layout


class PlotGUI():
    def __init__(self):
        self.window = sg.Window('Visualization', create_layout(), finalize=True,
                                element_justification='center', font='Helvetica 14')
        self.fig, self.ax = plt.subplots(figsize=(5, 5), dpi=100)

        self.fig_agg = draw_figure_w_toolbar(
            self.window['-CANVAS-'].TKCanvas, self.fig, self.window['-CONTROLS_CV-'].TKCanvas)
        self.points = self.ax.plot([], [], color="red", marker=".", ls="")[0]
        self.current_point = self.ax.plot([],[],color="green",ls="",marker=".")[0]
        self.ax.axis('equal')
