#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 20:19:54 2022

@author: cimps
"""

import time

import logging
logging.basicConfig(level=logging.INFO)

# simply import the module
import pycont.controller

# link to your config file
SETUP_CONFIG_FILE = './config.json'

# and load the config file in a MultiPumpController
controller = pycont.controller.MultiPumpController.from_configfile(SETUP_CONFIG_FILE)

# initialize the pumps in a smart way, if they are already initialized we do not want to reinitialize them because they go back to zero position
controller.smart_initialize()


# controller.pumps['water1'].go_to_volume(0, wait=True,speed=3000)
# t = time.time()
# controller.pumps['water3'].deliver(12.5, wait=True)
# total_time = time.time()-t

# controller.pumps['water2'].pump(12.5, wait=True,speed_in=6000)


# controller.pumps['water1'].set_valve_position('E')
# controller.pumps['water2'].set_valve_position('E')
# controller.pumps['water3'].set_valve_position('E')


def sucker(pump,speed,valve):
    controller.pumps[pump].set_valve_position(valve)
    controller.pumps[pump].go_to_volume(12.5, wait=True,speed=speed)
    
def sucker2(pump,speed,valve):
    controller.pumps[pump].set_valve_position(valve)
    controller.pumps[pump].go_to_volume(12.5, wait=False,speed=speed)    
    
def pumper(pump,speed,valve):
    controller.pumps[pump].set_valve_position(valve)
    controller.pumps[pump].go_to_volume(0, wait=True,speed=speed)
    
def pumper2(pump,speed,valve):
    controller.pumps[pump].set_valve_position(valve)
    controller.pumps[pump].go_to_volume(0, wait=False,speed=speed)

def temp():
    move_relative(0,0,-65)
    time.sleep(16)
    sucker("water1",3000)
    move_relative(0,0,65)
    time.sleep(16)
    move_relative(43,0,0)
    time.sleep(3)
    move_relative(0,0,-65)
    time.sleep(16)
    sucker("water2",3000)
    move_relative(0,0,65)
    time.sleep(16)
    move_relative(43,0,0)
    time.sleep(3)
    move_relative(0,0,-65)
    time.sleep(16)
    sucker("water3",3000)
    move_relative(0,0,65)
    time.sleep(16)

    
    
    
    
    
        
        

    

    




import serial
import time

printer_sport = "/dev/ttyUSB3"
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

ser= serial.Serial('/dev/ttyACM5',9600)

def red(state):
    if state is "top":
        ser.write(b'#22#22')
        ser.write(b'#33#33')
    if state is "center":
        ser.write(b'#2#2')
        ser.write(b'#33#33')
    if state is "down":
        ser.write(b'#22#22')
        ser.write(b'#3#3')


def green(state):
    if state is "top":
        ser.write(b'#44#44')
        ser.write(b'#55#55')
    if state is "center":
        ser.write(b'#4#4')
        ser.write(b'#55#55')
    if state is "down":
        ser.write(b'#44#44')
        ser.write(b'#5#5')
        


def blue(state):
    if state is "top":
        ser.write(b'#66#66')
        ser.write(b'#77#77')
    if state is "center":
        ser.write(b'#6#6')
        ser.write(b'#77#77')
    if state is "down":
        ser.write(b'#66#66')
        ser.write(b'#7#7')
        
        
def goto(dest):
    
    if dest is "red":
        move_relative(0,80,50)
        time.sleep(10)
        move_absolute(60,220,205)
        time.sleep(5)
    
    if dest is "green":
        move_relative(0,80,50)
        time.sleep(10)
        move_absolute(103,220,205)
        time.sleep(5)
    
    if dest is "blue":
        move_relative(0,80,50)
        time.sleep(10)
        move_absolute(146,220,205)
        time.sleep(5)
    
    if dest is "washing":
        move_relative(0,80,50)
        time.sleep(10)
        move_absolute(60,140,250)
        time.sleep(5)
    
    if dest is "waste":
        move_relative(0,80,50)
        time.sleep(10)
        move_absolute(150,140,230)
        time.sleep(5)
    


#redloc [60,220,205]
#gloc [103,220,205]
#bloc [146,220,205]
#washerloc [60,140,250]
#wasteloc [150,140,230]



#whole script

goto("red")
move_relative(0,0,-80)
time.sleep(19)
sucker("water1",5000,"E")
move_relative(0,0,80)
time.sleep(19)
sucker("water2",5000,"O")
pumper("water2",5000,"E")
sucker("water2",5000,"O")
pumper("water2",5000,"E")
goto("washing")
move_relative(0,0,-80)
time.sleep(19)
sucker("water2", 5000,"E")
move_relative(0,0,80)
time.sleep(19)
goto("waste")
pumper("water2",5000,"E")
goto("washing")
move_relative(0,0,-80)
time.sleep(19)
sucker("water2", 5000,"E")
move_relative(0,0,80)
time.sleep(19)
goto("waste")
pumper("water2",5000,"E")



goto("green")
move_relative(0,0,-80)
time.sleep(19)
sucker("water2",5000,"E")
move_relative(0,0,80)
time.sleep(19)
sucker("water3",5000,"O")
pumper("water3",5000,"E")
sucker("water3",5000,"O")
pumper("water3",5000,"E")
goto("washing")
move_relative(0,0,-80)
time.sleep(19)
sucker("water3", 5000,"E")
move_relative(0,0,80)
time.sleep(19)
goto("waste")
pumper("water3",5000,"E")
goto("washing")
move_relative(0,0,-80)
time.sleep(19)
sucker("water3", 5000,"E")
move_relative(0,0,80)
time.sleep(19)
goto("waste")
pumper("water3",5000,"E")



goto("blue")
move_relative(0,0,-80)
time.sleep(19)
sucker("water3",5000,"E")
move_relative(0,0,80)


time.sleep(10)
red("top")
green("center")
blue("down")
pumper2("water1",300,"I")
pumper2("water2",300,"I")
pumper2("water3",300,"I")
time.sleep(50)
red("center")
green("down")
blue("top")
time.sleep(50)
red("down")
green("top")
blue("center")

sucker2("water1",5000,"E")
sucker2("water2",5000,"E")
sucker2("water3",5000,"E")

goto("waste")
sucker2("water1",5000,"E")
sucker2("water2",5000,"E")
sucker2("water3",5000,"E")
time.sleep(5)
pumper2("water1",5000,"I")
pumper2("water2",5000,"I")
pumper2("water3",5000,"I")

goto("washing")
move_relative(0,0,-80)


for i in range(2):
    sucker2("water1",5000,"E")
    sucker2("water2",5000,"E")
    sucker2("water3",5000,"E")
    time.sleep(8)
    pumper2("water1",5000,"O")
    pumper2("water2",5000,"O")
    pumper2("water3",5000,"O")
    time.sleep(8)

sucker2("water3",5000,"E")

# ser.close()

for i in range(10):
    red("center")
    time.sleep(0.25)
    red("top")
    time.sleep(0.5)
    red("down")
    time.sleep(0.5)






    
        
    
