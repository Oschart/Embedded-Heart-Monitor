import serial

c = input('c = ')

s = serial.Serial(port="COM6", baudrate=115200,
                  bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
s.write(b'oscar')

res = s.read()
print(res)
res = s.read()
print(res)
res = s.read()
print(res)

