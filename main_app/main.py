import serial
import serial.tools.list_ports
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from app_utils import valid_input, uC_transmit, uC_receive

print('Welcome to my ECG application!')
# Get list of available ports
#comports_list = list(map(lambda p: p.device, serial.tools.list_ports.comports()))
#print('Available COM ports: ' + str(comports_list))
#com_port = valid_input('COM port = ', lambda p: p in comports_list)

#baud_rate = input('Baud rate (bps) = ')

serial_p = serial.Serial(port="COM6", baudrate=115200,
                  bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read heart pulse from uC
    beat = int(uC_receive(serial_p))

    if beat == -1:
        ani.event_source.stop()
        return
    elif beat == -2:
        beat = 512

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%S'))
    ys.append(beat)

    # Limit x and y lists to 20 items
    xs = xs[-30:]
    ys = ys[-30:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, color='r')

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Heart Activity')


while True:
    cmd = input('>> ').upper()
    uC_transmit(serial_p, cmd)
    if cmd == "C1MWD":
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xs = []
        ys = []
        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=200)
        plt.show()
    elif cmd == "RHBR":
        hr = uC_receive(serial_p)
        print('Heart beat rate = ' + hr + ' bpm')
    elif cmd == "EXIT":
        break


