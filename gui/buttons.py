import serial.tools.list_ports


def get_available_com_ports():
    ports = serial.tools.list_ports.comports()
    return [desc for (_, desc, _) in sorted(ports)]


def get_com_port_from_desc(com_port_desc):
    ports = serial.tools.list_ports.comports()
    for port, desc, _ in ports:
        if com_port_desc in desc:
            return port


def update_coordinate_inputs(input1, input2, values: list):
    input1.update(values[0])
    input2.update(values[1])
