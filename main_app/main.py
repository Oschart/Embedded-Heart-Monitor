import serial
import serial.tools.list_ports
from app_utils import valid_input, uC_transmit, uC_receive

print('Welcome to my ECG application!')
# Get list of available ports
#comports_list = list(map(lambda p: p.device, serial.tools.list_ports.comports()))
#print('Available COM ports: ' + str(comports_list))
#com_port = valid_input('COM port = ', lambda p: p in comports_list)

#baud_rate = input('Baud rate (bps) = ')

serial_p = serial.Serial(port="COM6", baudrate=115200,
                  bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

while True:
    cmd = input('>> ')
    uC_transmit(serial_p, cmd)
    full_res = uC_receive(serial_p)
    print(str(full_res))


serial_p.write(b'oscar')

res = serial_p.read()
print(res)
res = serial_p.read()
print(res)
res = serial_p.read()
print(res)

