def valid_input(prompt, is_valid):
    res = input(prompt)
    while not is_valid(res):
        print('Sorry, try again!')
        res = input(prompt)
    return res

def display_brief_guide():
    print('Supported Commands: ')
    print('SSR(R): -> Sets sampling rate to R')
    return
    
def uC_transmit(serial_p, cmd):
    # Send command string in byte mode
    cmd += '$'
    serial_p.write(cmd.encode())
    serial_p.flush()

def uC_receive(serial_p):
    res = serial_p.readline().decode()[:-1].replace('\x00', '')
    
    return res if res[0:2] != 'OK' else -1 
