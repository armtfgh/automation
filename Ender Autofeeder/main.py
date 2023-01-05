import tkinter as tk
import serial
import time
from threading import Timer

printer_sport = "/dev/ttyUSB0"
printer_port = serial.Serial(printer_sport, 115200, timeout=1)




REST_HEIGHT = 1000
HOME_LOC_X = 85
HOME_LOC_Y = 165
HOME_LOC_Z = 80
DEFAULT_PUMP_TIME="1"
CUP_SPACING=53



def send_cmd(cmd):
    print(cmd)
    printer_port.write(f"{cmd}\n".encode("ASCII"))

def autohome():
    send_cmd("G28")

def move(x=None, y=None, z=None):
    s = "G0"
    if x is not None:
        s += f"X{x}"
    if y is not None:
        s += f"Y{y}"
    if z is not None:
        s += f"Z{z}"
    
    s+= "F5000"
    send_cmd(s)


def move_relative(x=None, y=None, z=None):
    send_cmd("G91")
    move(x,y,z)

def move_absolute(x=None, y=None, z=None):
    send_cmd("G90")
    move(x,y,z)

def up_ten():
    move_relative(z=10)

def down_ten():
    move_relative(z=-10)

def go_home():
    move_absolute(x=HOME_LOC_X, y=HOME_LOC_Y, z=HOME_LOC_Z)


def runner():
    for i in range(4):
        move_relative(30,0,0)
        time.sleep(2)
        move_relative(0,0,-20)
        time.sleep(5)
        move_relative(0,0,20)
        time.sleep(3)
    move_relative(-120,-30,0)
    for i in range(4):
        move_relative(30,0,0)
        time.sleep(2)
        move_relative(0,0,-20)
        time.sleep(5)
        move_relative(0,0,20)
        time.sleep(3)
    move_relative(-120,-30,0)
    for i in range(4):
        move_relative(30,0,0)
        time.sleep(2)
        move_relative(0,0,-20)
        time.sleep(5)
        move_relative(0,0,20)
        time.sleep(3)
    move_relative(-120,-30,0)

    

    


        