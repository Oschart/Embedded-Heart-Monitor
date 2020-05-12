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
    res = serial_p.readline().decode()
    #res = res[1:]
    frst_read = True
    print(res)
    while res[0:2] != 'OK':
        if frst_read:
            res = res[0:]
        res = res[:-1]
        print(res)
        full_res.append(res)
        res = serial_p.readline().decode()
    return full_res
