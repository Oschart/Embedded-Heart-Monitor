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

ani, ax, values, x_cnt = None, None, None, 0
num_of_samples = 0
# action callbacks
def SSR():
    global num_of_samples
    X = values['srate']
    num_of_samples = int(X)*60
    print(X)
    print('number of samples = ', num_of_samples)
    cmd = 'SSR ' + X + '$'
    uC_transmit(serial_p, cmd)

def C1MWD():
    global ax, ani, x_cnt
    cmd = 'C1MWD$'
    uC_transmit(serial_p, cmd)
    x_cnt = 0
    fig = plt.figure(1,figsize=(15, 7), dpi=80)
    fig.canvas.mpl_connect('close_event', TEARUP)
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
    plt.show(block=False)

def RHBR():
    cmd = 'RHBR$'
    uC_transmit(serial_p, cmd)
    hbr = uC_receive(serial_p)
    if hbr == -2:
        hbr = '-'
    while hbr == -1:
        hbr = uC_receive(serial_p)
    window['HBR'].update(hbr)

def TEARUP(evt):
    global ani
    print('transmission tear-up!')
    uC_transmit(serial_p, '#')
    ani.event_source.stop()
    plt.close()
    res = uC_receive(serial_p)
    while res != -1:
        res = uC_receive(serial_p)


button_actions = {
    'SSR': SSR,
    'C1MWD': C1MWD,
    'RHBR': RHBR,
}

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # Check if figure window is still open
    if plt.fignum_exists(1) == False:
        return
    
    global ax, ani, x_cnt
    # Read heart pulse from uC
    beat = int(uC_receive(serial_p))
    print(beat)
    if beat == -1:
        ani.event_source.stop()
        return
    elif beat == -2:
        beat = 2048

    # Add x and y to lists
    xs.append(x_cnt)
    ys.append(beat)

    x_cnt = x_cnt+1
    # Limit x and y lists to 20 items
    #xs = xs[-30:]
    #ys = ys[-30:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, color='r', linewidth=0.5)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(num_of_samples*0.1))
    plt.gca().set_ylim([0, 4096])
    plt.gca().set_xlim([0, num_of_samples])
    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Heart Activity')
    # plt.grid()

while True:
    event, values = window.read()
    print(values)
    print(event)
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
                           size=(500, 500), element_justification='center')
    if event in button_actions:
        button_actions[event]()

window.close()