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


logging.basicConfig(level=logging.INFO)

# simply import the module


# link to your config file
SETUP_CONFIG_FILE = './config.json'

# and load the config file in a MultiPumpController
controller = pycont.controller.MultiPumpController.from_configfile(SETUP_CONFIG_FILE)

# initialize the pumps in a smart way, if they are already initialized we do not want to reinitialize them because they go back to zero position
controller.smart_initialize()


def speed(flowrate):
    return int(flowrate-0.029977)/0.015492

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

def pump_suck(pump,speed):
    controller.pumps[pump].go_to_volume(0, wait=True,speed=speed) 
    controller.pumps[pump].set_valve_position("I")
    controller.pumps[pump].go_to_volume(12.5, wait=False,speed=10000) 
    controller.pumps[pump].set_valve_position("E")


    
def synch(Q):
    sp = int(speed(Q))
    controller.pumps["inj1"].set_valve_position("I")
    controller.pumps["inj2"].set_valve_position("I")
    controller.pumps["inj1"].go_to_volume(12.5, wait=False,speed=10000) 
    controller.pumps["inj2"].go_to_volume(12.5, wait=False,speed=10000)
    state = "inj1"
    for i in range(3):
        if state is "inj1":
            pump_suck("inj2",sp)
            state = "inj2"
        elif state is "inj2":
            pump_suck("inj1",sp)
            state = "inj1"
            
                                                                                                                                          
for i in range(5):            
    controller.pumps["inj1"].set_valve_position("E")
    controller.pumps["inj1"].go_to_volume(0, wait=False,speed=5000) 
    controller.pumps["inj2"].set_valve_position("I")
    controller.pumps["inj2"].go_to_volume(12.5, wait=False,speed=10000)  
    while controller.pumps['inj1'].current_volume>0.5:
        continue
    controller.pumps["inj2"].set_valve_position("E")
    controller.pumps["inj2"].go_to_volume(0, wait=False,speed=5000) 
    controller.pumps["inj1"].set_valve_position("I")
    controller.pumps["inj1"].go_to_volume(12.5, wait=False,speed=10000)
    while controller.pumps['inj2'].current_volume>0.5:
        continue

 







    

    
 



