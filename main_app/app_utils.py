import serial
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import PySimpleGUI as sg



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

    return -2 if len(res) == 0 or res[0] == '!' else -1 if res[0:2] == 'OK' else res



def connect_layout(comports_list):
    return [[sg.Text('Connection Panel', font=('Verdana', 12))],
            [sg.Text('----------------')],
            [sg.Text('Select COM port: '), sg.Combo(comports_list, key='com', size=(10, 1))],
            [sg.Text('Baud Rate: '), sg.Input(key='baudrate', size=(10, 1))],
            [sg.Text('')],
            [sg.Button('Start', font=('Verdana', 12))],
            [sg.Text('')],
            [sg.Button('Exit', font=('Verdana', 12))]]

def control_layout():
    return [[sg.Text('Welcome!', font=('Verdana', 12))],
            [sg.Text('----------------')],
            [sg.Text('Control Panel', font=('Verdana', 12))],
            [sg.Text('----------------')],
            [sg.Text('Sampling Rate ', font=('Verdana', 12)), sg.Input(key='srate', size=(10, 5), 
            font=('Verdana', 12)), sg.Button(button_text='Set', font=('Verdana', 12), key='SSR')],
            [sg.Text('')],
            [sg.Button('Collect & Plot ECG for 1 Min', font=('Verdana', 12), key='C1MWD')],
            [sg.Text('')],
            [sg.Button('Report Heart Beat Rate', font=('Verdana', 12), key='RHBR')],
            [sg.Text('')],
            [sg.Text('Heart Beat Rate (bpm): ', font=('Verdana', 12)), sg.Text('-', font=('Verdana', 12), key='HBR')],
            [sg.Text('')],
            [sg.Button('Exit', font=('Verdana', 12))]
            ]
