import tkinter as tk
import serial
import time
from threading import Timer

printer_sport = "/dev/ttyUSB1"
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

    

    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 15:26:12 2022

@author: cimps
"""

import serial as serial 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import logging
import pycont.controller


try:
    motor = serial.Serial("/dev/ttyUSB9",baudrate=9600,timeout=.1)
except:
    motor.close()
    motor = serial.Serial("/dev/ttyUSB9",baudrate=9600,timeout=.1)



try:
    valve = serial.Serial("/dev/ttyACM1",baudrate=9600,timeout=.1)
except:
    valve.close()
    valve = serial.Serial("/dev/ttyACM1",baudrate=9600,timeout=.1)


import time


logging.basicConfig(level=logging.INFO)

# simply import the module


# link to your config file
SETUP_CONFIG_FILE = './config.json'

# and load the config file in a MultiPumpController
controller = pycont.controller.MultiPumpController.from_configfile(SETUP_CONFIG_FILE)

# initialize the pumps in a smart way, if they are already initialized we do not want to reinitialize them because they go back to zero position
controller.smart_initialize()


def speed(flowrate):
    return (flowrate-0.029977)/0.015492

def sucker(pump,speed,valve):
    controller.pumps[pump].set_valve_position(valve)
    controller.pumps[pump].go_to_volume(12.5, wait=True,speed=speed)
    
def sucker2(pump,speed,valve):
    controller.pumps[pump].set_valve_position(valve)
    controller.pumps[pump].go_to_volume(12.5, wait=False,speed=speed)    
    
def pumper(pump,speed,valve):
    controller.pumps[pump].set_valve_position(valve)
    controller.pumps[pump].go_to_volume(0, wait=True,speed=speed)
    
def pumper2(pump,speed,pos,valve):
    controller.pumps[pump].set_valve_position(valve)
    controller.pumps[pump].go_to_volume(pos, wait=True,speed=speed)


move_absolute(98,140,161)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(4, wait=True,speed=100)





#script first
move_absolute(17,140,162)
time.sleep(13)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
move_absolute(17,140,210)
time.sleep(13)
move_absolute(17,113,210)
time.sleep(8)
controller.pumps["inj"].set_valve_position("I")
controller.pumps["inj"].go_to_volume(7.5, wait=True,speed=11)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)

#washing
move_absolute(17,113,240)
time.sleep(15)
move_absolute(92,70,240)
time.sleep(8)
move_absolute(92,70,180)
time.sleep(20)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
move_absolute(92,70,240)
time.sleep(20)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)






#script second
x,y = 44,140
move_absolute(x,y,210)
time.sleep(20)
move_absolute(x,y,162)
time.sleep(13)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
move_absolute(x,140,210)
time.sleep(13)
move_absolute(x,113,210)
time.sleep(8)
controller.pumps["inj"].set_valve_position("I")
controller.pumps["inj"].go_to_volume(7.5, wait=True,speed=11)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)

#washing
move_absolute(x,113,240)
time.sleep(15)

move_absolute(92,70,240)
time.sleep(18)

move_absolute(92,70,180)
time.sleep(20)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
move_absolute(92,70,240)
time.sleep(18)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)



#script third
x,y = 71,140
move_absolute(x,y,210)
time.sleep(20)
move_absolute(x,y,162)
time.sleep(13)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
move_absolute(x,140,210)
time.sleep(13)
move_absolute(x,113,210)
time.sleep(8)
controller.pumps["inj"].set_valve_position("I")
controller.pumps["inj"].go_to_volume(7.5, wait=True,speed=11)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)

#washing
move_absolute(x,113,240)
time.sleep(15)

move_absolute(92,70,240)
time.sleep(18)

move_absolute(92,70,180)
time.sleep(20)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
move_absolute(92,70,240)
time.sleep(18)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)





#script 4th
x,y = 98,140
move_absolute(x,y,210)
time.sleep(20)
move_absolute(x,y,162)
time.sleep(13)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
move_absolute(x,140,210)
time.sleep(13)
move_absolute(x,113,210)
time.sleep(8)
controller.pumps["inj"].set_valve_position("I")
controller.pumps["inj"].go_to_volume(7.5, wait=True,speed=11)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)

#washing
move_absolute(x,113,240)
time.sleep(15)

move_absolute(122,70,240)
time.sleep(18)

move_absolute(122,70,180)
time.sleep(20)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
move_absolute(122,70,240)
time.sleep(18)
controller.pumps["inj"].set_valve_position("O")
controller.pumps["inj"].go_to_volume(0, wait=True,speed=10000)
controller.pumps["inj"].set_valve_position("E")
controller.pumps["inj"].go_to_volume(12.5, wait=True,speed=10000)
















