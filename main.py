import PySimpleGUI as sg
from scanner import main as scanner_main
from position import main as position_main

if __name__ == "__main__":
    layout = [
        [sg.B("Point Converter", key="-CONVERTER-"),
         sg.B("Scanner", key="-SCANNER-")]
    ]
    window = sg.Window("Solis-XY", layout=layout,
                       finalize=True, font=("Verdana", "12"))

    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "-SCANNER-":
            scanner_main()

        if event == '-CONVERTER-':
            position_main()
