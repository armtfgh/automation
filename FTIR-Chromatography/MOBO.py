# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:01:04 2022

@author: 박 채현
"""




# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 21:17:12 2022

@author: 박 채현
"""


import serial as serial 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import logging
import pycont 
import threading
from PIL import Image






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
    controller.pumps[pump].go_to_volume(pos, wait=False,speed=speed)

def pump_suck(pump,speed):
    controller.pumps[pump].go_to_volume(0, wait=True,speed=speed) 
    controller.pumps[pump].set_valve_position("I")
    controller.pumps[pump].go_to_volume(12.5, wait=False,speed=10000) 
    controller.pumps[pump].set_valve_position("E")



def new_init_auto():
    controller.pumps["inj1"].set_valve_position("E")
    controller.pumps["inj2"].set_valve_position("E")
    thf_pump.write(b'stop\r\n')
    samp_pump.write(b'stop\r\n')
    time.sleep(2)
    controller.pumps["inj1"].terminate()
    time.sleep(2)
    controller.pumps["inj2"].terminate()
    for i in range(2):
        new_init()
        time.sleep(2)
        controller.pumps["inj1"].terminate()
        time.sleep(2)
        controller.pumps["inj2"].terminate()
        time.sleep(2)
        
    new_init()
    

    
    
        


 
def samsung_pump(n,flowrate):
    spd = int(speed(flowrate))
    controller.pumps["inj1"].set_valve_position("E")
    controller.pumps["inj2"].set_valve_position("E")
    controller.pumps["inj1"].go_to_volume(12.5, wait=False,speed=10000)  
    controller.pumps["inj2"].go_to_volume(12.5, wait=True,speed=10000)     
    controller.pumps["inj1"].go_to_volume(9, wait=False,speed=10000)  
    controller.pumps["inj2"].go_to_volume(9, wait=True,speed=10000)  
    controller.pumps["inj1"].go_to_volume(12.5, wait=False,speed=5000)  
    controller.pumps["inj2"].go_to_volume(12.5, wait=True,speed=5000) 
  
    for i in range(n):            
        controller.pumps["inj1"].set_valve_position("I")
        controller.pumps["inj1"].go_to_volume(0, wait=False,speed=spd) 
        controller.pumps["inj2"].set_valve_position("E")
        controller.pumps["inj2"].go_to_volume(12.5, wait=False,speed=3000)  
        while controller.pumps['inj1'].current_volume>0.5:
            continue
        controller.pumps["inj2"].set_valve_position("I")
        controller.pumps["inj2"].go_to_volume(0, wait=False,speed=spd) 
        controller.pumps["inj1"].set_valve_position("E")
        controller.pumps["inj1"].go_to_volume(12.5, wait=False,speed=3000)
        while controller.pumps['inj2'].current_volume>0.5:
            continue



samp_pump = serial.Serial("COM14",9600)
valve = serial.Serial("COM12",9600)
thf_pump = serial.Serial("COM11",9600)



   
def smart_stopping():
    while True:
        thf_pump.write(b'stop\r\n')
        samp_pump.write(b'stop\r\n')
        controller.pumps["inj1"].terminate()
        time.sleep(2)
        controller.pumps["inj2"].terminate()
        new_init()
        time.sleep(2)
        if controller.pumps["inj1"].is_busy() or controller.pumps["inj1"].is_busy():
            controller.pumps["inj1"].terminate()
            controller.pumps["inj2"].terminate()
        else:
            break
    
    
#sample loading 
def load_sample(conc,amount):

    valve.write(b'#33#33')
    valve.write(b'#2#2')
    R = (c1-conc/conc)
    q_samp = q/(R+1)
    q_sol = q_samp*R
    q_hex = q_sol*(40/41)
    q_thf = q_sol*(1/41)
    thf_pump.write(('irate '+str(q_thf)+' ml/min\r\n').encode()) 
    samp_pump.write(('irate '+str(q_samp)+' ml/min\r\n').encode()) 
    thread = threading.Thread(target = samsung_pump,args = (1,q_hex))
    thread.start()
    # samsung_pump(1, q_hex)
    thf_pump.write(b'irun\r\n') 
    samp_pump.write(b'irun\r\n')     
    t_amount = 60*amount/q
    qt = q_sol+q_hex+q_thf
    tt = (vt/qt)*60
    time.sleep(tt*2)
    valve.write(b'#22#22')
    valve.write(b'#3#3')
    time.sleep(1.1*t_amount)
    valve.write(b'#33#33')
    valve.write(b'#2#2')
    thf_pump.write(b'stop\r\n')
    samp_pump.write(b'stop\r\n')
    controller.pumps["inj1"].terminate()
    controller.pumps["inj2"].terminate()
    
def new_init():
    controller.smart_initialize()
    controller.pumps["inj1"].set_valve_position("E")
    controller.pumps["inj2"].set_valve_position("E")

    controller.pumps["inj1"].go_to_volume(0, wait=False,speed=5000) 
    controller.pumps["inj2"].go_to_volume(0, wait=True,speed=5000) 
    
   


def elution_buffer(flowrate,n1):

    valve.write(b'#2#2')
    valve.write(b'#33#33')
    q_hex = flowrate*(40/41)
    q_thf = flowrate*(1/41)
    thf_pump.write(('irate '+str(q_thf)+' ml/min\r\n').encode())
    thf_pump.write(b'irun\r\n')
    thread = threading.Thread(target = samsung_pump,args = (n1,q_hex))
    thread.start()
    time.sleep(1.5*(5/flowrate)*60)
    valve.write(b'#22#22')
    valve.write(b'#3#3')   #here i did this 
    while True:
        if not controller.pumps["inj1"].is_busy() and not controller.pumps["inj2"].is_busy():
            break
    
    thf_pump.write(b'stop\r\n') 



def elution_buffer2(flowrate,n1):

    valve.write(b'#22#22')
    valve.write(b'#3#3')
    q_hex = flowrate*(40/41)
    q_thf = flowrate*(1/41)
    thf_pump.write(('irate '+str(q_thf)+' ml/min\r\n').encode())
    thf_pump.write(b'irun\r\n')
    thread = threading.Thread(target = samsung_pump,args = (n1,q_hex))
    thread.start()
 #here i did this 
    while True:
        if not controller.pumps["inj1"].is_busy() and not controller.pumps["inj2"].is_busy():
            break
    
    thf_pump.write(b'stop\r\n') 

    
def overlap(l1,l2):
    s=0
    for i in range(len(l1)):
        if l1[i]>0 and l2[i]>0:
            s+=1
    l3 = [i for i in l1 if i>0]
    ref = int(len(l3))
    return s/ref

# #script
# time.sleep(5)
# q1 = 2
# elution_buffer(2)
# ys = []
# state  = []
# while True:
#     img = pyautogui.screenshot('my_screenshot.png')
#     img_cropped = img.crop((65,54,1276,754))
#     x_data, y_data = get_data(ims3,1000,1500,110,0)
#     peak = np.max(y_data[300:320])
#     ys.append(peak)
#     if peak>thresh:
#         state.append(1)
#     elif peak<=thres:
#         state.append(0)
#     if len(ys)>50 and sum(state)>10 and sum(state[-10:-1])<4:
#         break
#     time.sleep(2)

#run the elution buffer for analysis       
thread2 = threading.Thread(target = elution_buffer2,args = (10,2))
thread2.start()   
##############################################
from PIL import Image
import numpy as np
import pyautogui
import time

def get_data(im, x_range, x_offset, y_range, y_offset):
    x_data = np.array([])
    y_data = np.array([])
    width, height = im.size
    im = im.convert('1')
    for x in range(width):
        for y in range(height):
            if im.getpixel((x, y)) == 0:
                x_data = np.append(x_data, x)
                y_data = np.append(y_data, height - y)
                break
    x_data = (x_data / width) * x_range + x_offset
    y_data = (y_data / height) * y_range + y_offset
    return x_data, y_data
# pyautogui.mouseInfo()
def capture():
    Y1,Y2 = [],[]    
    time.sleep(5)    
    y1s,y2s = [],[]    
    started = False
    started1 = False
    started2 = False 
    finished = False    
    while True:
        shot =  pyautogui.screenshot('my_screenshot.png')
        shot = shot.crop((90,60,1267,739))
        x_data, y_data = get_data(shot,1000,1500,1.1,-0.14)
        Y1.append(y_data)
        y1_max = max(y_data[400:520])
        y2_max = max(y_data[800:900])
        y1s.append(y1_max)
        y2s.append(y2_max)
        if not started1 and y1_max>0:
            started1 = True
        if not started2 and y2_max>0:
            started2 = True
        
        if not started and started1 and started2:
            started = True
            print("process started")
        
        if started and np.average(y2s[-10:-1])<0 and y2s[-1]<0 and started2:
            print("process Fininhed")
            break
            
        time.sleep(2)
    time.sleep(100)
    thf_pump.write(b'stop\r\n') 
    samp_pump.write(b'stop\r\n') 
    controller.pumps["inj1"].terminate()
    controller.pumps["inj2"].terminate()
    res = overlap(y1s,y2s)
    thrp1 = len([i for i in y1s if i>0])
    thrp2 = len([i for i in y2s if i>0])
    thrp = thrp1+thrp2-res
    
    return res,thrp,y1s,y2s
##################################################################################     

     
c1  =  10 #sample concentration 
q = 10   #flowrate for sample loading 
vt = 5   #volume of all tubing 
 
def func(sample_amount,sample_conc,elution_flowrate):
    
    load_sample(sample_conc,sample_amount)
    thread2 = threading.Thread(target = elution_buffer,args = (elution_flowrate,2))
    thread2.start()
    time.sleep(1.5*(5/elution_flowrate)*60)
    res , thrp,y1s,y2s= capture()
    new_init_auto()
    
    return res , thrp,y1s,y2s

S = [1,2,3]
CC = [1,2,3]
E = [5,6,7]
RES = []
THRp = []
Y1s=[]
Y2s = []

for i in range(len(S)):
    a,b,c,d = func(S[i],CC[i],E[i])
    RES.append(a)
    THRp.append(b)
    Y1s.append(c)
    Y2s.append(d)

Y1,Y2 = [],[]    
time.sleep(1.5)    
y1s,y2s = [],[]    
started = False
started1 = False
started2 = False 
finished = False    
while True:
    shot =  pyautogui.screenshot('my_screenshot.png')
    shot = shot.crop((90,60,1267,739))
    x_data, y_data = get_data(shot,1000,1500,1.1,-0.14)
    Y1.append(y_data)
    y1_max = max(y_data[400:600])
    y2_max = max(y_data[750:950])
    y1s.append(y1_max)
    y2s.append(y2_max)
    if not started1 and y1_max>0:
        started1 = True
    if not started2 and y2_max>0:
        started2 = True
    
    if not started and started1 and started2:
        started = True
        print("process started")
    
    if started and np.average(y2s[-10:-1])<0 and y2s[-1]<0 and started2:
        print("process Fininhed")
        break
        
    time.sleep(2)
time.sleep(100)
thf_pump.write(b'stop\r\n') 
samp_pump.write(b'stop\r\n') 
controller.pumps["inj1"].terminate()
controller.pumps["inj2"].terminate()
res = overlap(y1s,y2s)
thrp1 = len([i for i in y1s if i>0])
thrp2 = len([i for i in y2s if i>0])
thrp = thrp1+thrp2-res
import matplotlib.pyplot as plt 

plt.plot(y1s)
plt.plot(y2s)



a,b,c,d = func(1,9.5,7)



