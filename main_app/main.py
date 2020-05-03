import serial
import serial.tools.list_ports
from app_utils import valid_input 

print('Welcome to my ECG application!')
# Get list of available ports
comports_list = list(map(lambda p: p.device, serial.tools.list_ports.comports()))
print('Available COM ports: ' + str(comports_list))

com_port = valid_input('COM port = ', lambda p: p in comports_list)
baud_rate = input('Baud rate (bps) = ')
sample_rate = input('Sampling rate (SPS) = ')

serial_p = serial.Serial(port="COM6", baudrate=115200,
                  bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

COM = input('COM port = ')
c = input('c = ')


s.write(b'oscar')

res = s.read()
print(res)
res = s.read()
print(res)
res = s.read()
print(res)

