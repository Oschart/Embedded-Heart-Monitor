import serial
import serial.tools.list_ports
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker

import PySimpleGUI as sg

from app_utils import *

print('Welcome to my ECG application!')

# Get list of available ports
comports_list = list(
    map(lambda p: p.device, serial.tools.list_ports.comports()))

sg.theme('DarkAmber')  # Add a touch of color


window = sg.Window('ECG Heart Monitor', connect_layout(comports_list),
                   size=(400, 250), element_justification='center')

ani, ax = None, None
# action callbacks
def SSR():
    X = values['srate']
    cmd = 'SSR ' + X + '$'
    uC_transmit(serial_p, cmd)

def C1MWD():
    global ax, ani
    cmd = 'C1MWD$'
    uC_transmit(serial_p, cmd)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
    plt.show()

def RHBR():
    cmd = 'RHBR$'
    uC_transmit(serial_p, cmd)

def TEARUP():
    cmd = 'TEARUP$'
    uC_transmit(serial_p, cmd)

button_actions = {
    'SSR': SSR,
    'C1MWD': C1MWD,
    'RHBR': RHBR,
    'TEARUP': TEARUP
}

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    global ax, ani
    # Read heart pulse from uC
    beat = int(uC_receive(serial_p))
    print(beat)
    if beat == -1:
        ani.event_source.stop()
        return
    elif beat == -2:
        beat = 2048

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%M:%S'))
    ys.append(beat)

    # Limit x and y lists to 20 items
    #xs = xs[-30:]
    #ys = ys[-30:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, color='r')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.gca().set_ylim([0, 4096])
    plt.gca().set_xlim([0, 80])
    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Heart Activity')
    # plt.grid()

while True:
    event, values = window.read()
    print(values)
    if event in (None, 'Exit'):     # if user closes window or clicks exit
        break
    if event == 'Start':  
        com_port = values['com']
        baud_rate = int(values['baudrate'])
        # Open the serial port
        serial_p = serial.Serial(port=com_port, baudrate=baud_rate,
                                 bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        # Initiate control panel layout
        window.close()
        window = sg.Window('ECG Heart Monitor', control_layout(),
                           size=(500, 400), element_justification='center')
    if event in button_actions:
        button_actions[event]()

window.close()