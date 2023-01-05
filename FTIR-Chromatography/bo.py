# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:58:06 2022

@author: 박 채현
"""



from edbo.plus.optimizer_botorch import EDBOplus
import numpy as np

reaction_components = {
    'amount': np.arange(0.5,2.15,0.15),
    'Conc': np.arange(5,10.5,0.5),
    'elution': np.arange(5,10,1),
}

EDBOplus().generate_reaction_scope(
    components=reaction_components, 
    filename='my_optimization.csv',
    check_overwrite=False
)


import pandas as pd
df_scope = pd.read_csv('my_optimization.csv')  # Load csv file.

n_combinations = len(df_scope)
print(f"Your reaction scope has {n_combinations} combinations.")

EDBOplus().run(
    filename='my_optimization.csv',  # Previously generated scope.
    objectives=['res', 'thrp'],  # Objectives to be optimized.
    objective_mode=['min', 'max'],  # Maximize yield and ee but minimize side_product.
    batch=1,  # Number of experiments in parallel that we want to perform in this round.
    columns_features='all', # features to be included in the model.
    init_sampling_method='cvtsampling'  # initialization method.
)
df_edbo = pd.read_csv('my_optimization.csv')
df_edbo.head(5)

df_edbo_round4.loc[0, 'res'] = 0.81
df_edbo_round4.loc[0, 'thrp'] = 0.08

df_edbo_round4.to_csv('my_optimization_round5.csv', index=False)

EDBOplus().run(
    filename='my_optimization_round5.csv',  # Previous scope (including observations).
    objectives=['res', 'thrp'],  # Objectives to be optimized.
    objective_mode=['min', 'max'],  # Maximize yield and ee but minimize side_product.
    batch=1,  # Number of experiments in parallel that we want to perform in this round.
    columns_features='all', # features to be included in the model.
    init_sampling_method='cvtsampling'  # initialization method.
)


df_edbo_round5 = pd.read_csv('my_optimization_round5.csv')
df_edbo_round5.head(5)


for i in range(5,20):
    EDBOplus().run(
        filename='my_optimization_round'+str(i)+'.csv',  # Previous scope (including observations).
        objectives=['res', 'thrp'],  # Objectives to be optimized.
        objective_mode=['min', 'max'],  # Maximize yield and ee but minimize side_product.
        batch=1,  # Number of experiments in parallel that we want to perform in this round.
        columns_features='all', # features to be included in the model.
        init_sampling_method='cvtsampling'  # initialization method.
    )
    df = pd.read_csv('my_optimization_round'+str(i)+'.csv')
    amount = df["amount"][0]
    conc = df["Conc"][0]
    elut= df["elution"][0]
    #process
    
    df.loc[0, 'res'] = 0.81
    df.loc[0, 'thrp'] = 0.08
    
    df.to_csv('my_optimization_round'+str(i+1)+'.csv')
    









#############################################################################

# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 17:16:34 2022

@author: 박 채현
"""

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

   
hex_pump1 = serial.Serial("COM10",9600)
hex_pump2=serial.Serial("COM15",9600)
valve = serial.Serial("COM12",9600)
thf_pump = serial.Serial("COM11",9600)
samp_pump = serial.Serial("COM14",9600)

  
#sample loading 
def load_sample(conc,amount):

    valve.write(b'#33#33')  #column
    valve.write(b'#2#2')  #waste
    R = (c1-conc/conc)
    q_samp = q/(R+1)
    q_sol = q_samp*R
    q_hex = q_sol*(40/41)
    q_thf = q_sol*(1/41)
    thf_pump.write(('irate '+str(q_thf)+' ml/min\r\n').encode()) 
    samp_pump.write(('irate '+str(q_samp)+' ml/min\r\n').encode()) 
    hex_pump1.write(('irate '+str(q_hex/4)+' ml/min\r\n').encode()) 
    hex_pump2.write(('irate '+str(q_hex/4)+' ml/min\r\n').encode()) 
    # samsung_pump(1, q_hex)
    thf_pump.write(b'irun\r\n') 
    samp_pump.write(b'irun\r\n')  
    hex_pump1.write(b'irun\r\n')     
    hex_pump2.write(b'irun\r\n')     
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
    hex_pump1.write(b'stop\r\n')
    hex_pump2.write(b'stop\r\n')


    
   


def elution_buffer(flowrate,vol):

    valve.write(b'#2#2')
    valve.write(b'#33#33')
    q_hex = flowrate*(40/41)
    q_thf = flowrate*(1/41)
    thf_pump.write(('irate '+str(q_thf)+' ml/min\r\n').encode())
    hex_pump1.write(('irate '+str(q_hex/4)+' ml/min\r\n').encode()) 
    hex_pump2.write(('irate '+str(q_hex/4)+' ml/min\r\n').encode())
    thf_pump.write(b'irun\r\n')
    hex_pump1.write(b'irun\r\n')
    hex_pump2.write(b'irun\r\n')
    
    time.sleep(1.5*(5/flowrate)*60)
    valve.write(b'#22#22')
    valve.write(b'#3#3')   #here i did this     
    time.sleep((vol/flowrate)*60)
    
    thf_pump.write(b'stop\r\n') 
    hex_pump1.write(b'stop\r\n') 
    hex_pump2.write(b'stop\r\n') 
    
def elution_buffer_inf(flowrate):

    valve.write(b'#2#2')
    valve.write(b'#33#33')
    q_hex = flowrate*(40/41)
    q_thf = flowrate*(1/41)
    thf_pump.write(('irate '+str(q_thf)+' ml/min\r\n').encode())
    hex_pump1.write(('irate '+str(q_hex/4)+' ml/min\r\n').encode()) 
    hex_pump2.write(('irate '+str(q_hex/4)+' ml/min\r\n').encode())
    thf_pump.write(b'irun\r\n')
    hex_pump1.write(b'irun\r\n')
    hex_pump2.write(b'irun\r\n')
    
    time.sleep(1.5*(5/flowrate)*60)
    valve.write(b'#22#22')
    valve.write(b'#3#3')   #here i did this     

def elution_buffer_fast(flowrate,vol):

    valve.write(b'#3#3')
    valve.write(b'#22#2')
    q_hex = flowrate*(40/41)
    q_thf = flowrate*(1/41)
    thf_pump.write(('irate '+str(q_thf)+' ml/min\r\n').encode())
    hex_pump1.write(('irate '+str(q_hex/4)+' ml/min\r\n').encode()) 
    hex_pump2.write(('irate '+str(q_hex/4)+' ml/min\r\n').encode())
    thf_pump.write(b'irun\r\n')
    hex_pump1.write(b'irun\r\n')
    hex_pump2.write(b'irun\r\n')
    
  
    time.sleep((vol/flowrate)*60)
    
    thf_pump.write(b'stop\r\n') 
    hex_pump1.write(b'stop\r\n') 
    hex_pump2.write(b'stop\r\n') 





    
def overlap(l1,l2):
    s=0
    for i in range(len(l1)):
        if l1[i]>val and l2[i]>val:
            s+=1
    l3 = [i for i in l1 if i>val]
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
thread2 = threading.Thread(target = elution_buffer_fast,args = (5,20))
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
val = -0.02
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
        if len(y_data)>0:
            y1_max = max(y_data[400:520])
            y2_max = max(y_data[800:900])
            y1s.append(y1_max)
            y2s.append(y2_max)
        if not started1 and y1_max>val:
            started1 = True
        if not started2 and y2_max>val:
            started2 = True
        
        if not started and started1 and started2:
            started = True
            print("process started")
        
        if started and np.average(y2s[-10:-1])<val and y2s[-1]<val and started2:
            print("process Fininhed")
            break
            
        time.sleep(2)
    time.sleep(100)
    thf_pump.write(b'stop\r\n') 
    samp_pump.write(b'stop\r\n') 
    hex_pump1.write(b'stop\r\n') 
    hex_pump2.write(b'stop\r\n') 

    res = overlap(y1s,y2s)
    thrp1 = len([i for i in y1s if i>val])
    thrp2 = len([i for i in y2s if i>val])
    thrp = thrp1+thrp2-res
    
    return res,thrp,y1s,y2s
##################################################################################     

     
c1  =  10 #sample concentration 
q = 10   #flowrate for sample loading 
vt = 5   #volume of all tubing 
 
def func(sample_amount,sample_conc,elution_flowrate):
    
    load_sample(sample_conc,sample_amount)
    thread2 = threading.Thread(target = elution_buffer_inf,args = (elution_flowrate,))
    thread2.start()
    time.sleep(1.5*(5/elution_flowrate)*60)
    res , thrp,y1s,y2s= capture()

    
    return res , thrp,y1s,y2s



Y1s = []
Y2s=[]
EDBOplus().run(
    filename='my_optimization.csv',  # Previous scope (including observations).
    objectives=['res', 'thrp'],  # Objectives to be optimized.
    objective_mode=['min', 'max'],  # Maximize yield and ee but minimize side_product.
    batch=1,  # Number of experiments in parallel that we want to perform in this round.
    columns_features='all', # features to be included in the model.
    init_sampling_method='cvtsampling'  # initialization method.
)
df = pd.read_csv('my_optimization.csv')
amount = df["amount"][0]
conc = df["Conc"][0]
elut= df["elution"][0]
res,thrp,y1s,y2s = func(amount,conc,elut)
df.loc[0, 'res'] = res
df.loc[0, 'thrp'] = (conc*amount)/thrp
Y1s.append(y1s)
Y2s.append(y2s)
df.to_csv('my_optimization_round0.csv')   


for i in range(3,10):
    EDBOplus().run(
        filename='my_optimization_round'+str(i)+'.csv',  # Previous scope (including observations).
        objectives=['res', 'thrp'],  # Objectives to be optimized.
        objective_mode=['min', 'max'],  # Maximize yield and ee but minimize side_product.
        batch=1,  # Number of experiments in parallel that we want to perform in this round.
        columns_features='all', # features to be included in the model.
        init_sampling_method='cvtsampling'  # initialization method.
    )
    df = pd.read_csv('my_optimization_round'+str(i)+'.csv')
    amount = df["amount"][0]
    conc = df["Conc"][0]
    elut= df["elution"][0]
    #process
    res,thrp,y1s,y2s = func(amount,conc,elut)
    df.loc[0, 'res'] = res
    df.loc[0, 'thrp'] = (conc*amount)/thrp
    Y1s.append(y1s)
    Y2s.append(y2s)
    df.to_csv('my_optimization_round'+str(i+1)+'.csv')   
    
import matplotlib.pyplot as plt 
    
for i in range(10):
    plt.figure()
    plt.plot(Y1s[i])
    plt.plot(Y2s[i])
    plt.title("round"+str(i))   