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
import time


try:
    motor = serial.Serial("/dev/ttyACM0",baudrate=9600,timeout=.1)
except:
    motor.close()
    motor = serial.Serial("/dev/ttyACM0",baudrate=9600,timeout=.1)



try:
    valve = serial.Serial("/dev/ttyACM4",baudrate=9600,timeout=.1)
except:
    valve.close()
    valve = serial.Serial("/dev/ttyACM4",baudrate=9600,timeout=.1)




logging.basicConfig(level=logging.INFO)

# simply import the module


# link to your config file
SETUP_CONFIG_FILE = './config1.json'

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
    

pumper("washer",5000,"I")
motor.write(b'd18000')
sucker("solvent",5000,"O")
controller.pumps["solvent"].set_valve_position("E")
controller.pumps["solvent"].go_to_volume(0, wait=True,speed=5000)
motor.write(b'u18000')

def initialize():
    sucker("solvent",5000,"O")
    controller.pumps["solvent"].go_to_volume(10, wait=True,speed=5000)
    sucker("solvent",5000,"O")
    controller.pumps["washer"].set_valve_position("I")
    controller.pumps["washer"].go_to_volume(0, wait=True,speed=10000)
    
def washing(n,vol):
    initialize()
    for i in range(n):
        if controller.pumps['solvent'].is_volume_pumpable(vol):
            motor.write(b'd18200')
            time.sleep(1)
            sucker("washer",5000,"O")
            pumper("washer",10000,"I")
            motor.write(b'u18200')
            time.sleep(4.5)
            pos = float(controller.pumps['solvent'].current_volume)
            controller.pumps["solvent"].set_valve_position("E")
            controller.pumps["solvent"].go_to_volume(pos-vol, wait=True,speed=5000)
        else:
            sucker("solvent",5000,"O")
            motor.write(b'd18200')
            time.sleep(1)
            sucker("washer",5000,"O")
            pumper("washer",10000,"I")
            motor.write(b'u18200')
            time.sleep(4.5)
            pos = float(controller.pumps['solvent'].current_volume)
            controller.pumps["solvent"].set_valve_position("E")
            controller.pumps["solvent"].go_to_volume(pos-vol, wait=True,speed=5000)
    
            
    motor.write(b'd18200')
    motor.write(b'd18200')
    time.sleep(1)
    sucker("washer",5000,"O")
    pumper("washer",10000,"I")
    motor.write(b'u18200')
   
            
            
            
#calibration of the pumps 
def calibrator():
    speeds = [200,500,800,1000,1500,2000,2500,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000]
    times = []
    
    for i in speeds:
        sucker("solvent",10000,"O")
        t = time.time()
        pumper("solvent",i,"O")
        times.append(time.time()-t)
        
    df = pd.DataFrame()
    
    df["speeds"]= np.asarray(speeds)
    df["times"] = np.asarray(times)
    
    df.to_csv("cont_calib.csv")
        
        
#batch one

valve.write(b'#3#3')
sucker2("polymer",5000,"O")
sucker2("anti",5000,"O")
pol_FR = 2
anti_FR = 2
pol_speed= int(speed(pol_FR))
anti_speed= int(speed(pol_FR))
controller.pumps["polymer"].set_valve_position("E")
controller.pumps["anti"].set_valve_position("E")
controller.pumps["polymer"].go_to_volume(6.5, wait=False,speed=pol_speed)
controller.pumps["anti"].go_to_volume(6.5, wait=False,speed=pol_speed)
time.sleep(10)
valve.write(b'#33#33')
valve.write(b'#2#2')
time.sleep(30)
valve.write(b'#22#22')
valve.write(b'#3#3')

while float(controller.pumps['polymer'].current_volume)>6.5:
    pass
motor.write(b'd18200')
time.sleep(1)
sucker("washer",5000,"O")









pumpss = ["polymer","anti","washer","solvent"]
for i in pumpss:
    controller.pumps[i].terminate()

