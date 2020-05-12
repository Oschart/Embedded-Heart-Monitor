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
    full_res = []
    res = serial_p.readline().decode()[:-1]
    #res = res[1:]
    print(res)
    while res[0:2] != 'OK':
        # Filter escape character
        if '\x00' in res:
            res = res[1:]
        full_res.append(res)
        res = serial_p.readline().decode()[:-1]
        print(res)
    return full_res
