from PIL import Image
import numpy as np
import pyautogui
import time
import pandas as pd

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


# im = Image.open('img.png')
df = pd.DataFrame()
# from pylab import *
# plot(x_data, y_data)
# grid(True)
# savefig('new_data.png')
# show()
Y = []
X = []
time.sleep(5)
for i in range(1800):
# ims1 = pyautogui.screenshot(region=(1351,590,1914,984))
# ims1.show()
# ims1.save("imggg1.png")
    ims2 = pyautogui.screenshot('my_screenshot.png')
    ims3 = ims2.crop((90,60,1267,739))
    x_data, y_data = get_data(ims3,1000,1500,1.1,-0.14)
    # df["y"+str(i)] = y_data
    Y.append(y_data)
    X.append(x_data)
    time.sleep(2)
    
    # ims3.show()
# pyautogui.mouseInfo()