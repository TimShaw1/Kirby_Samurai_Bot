from utility import *
import copy
import keyboard
import time
from ctypes import windll
dc= windll.user32.GetDC(0)

def getpixel(x,y):
    return tuple(int.to_bytes(windll.gdi32.GetPixel(dc,x,y), 3, "little"))

dim = get_dimensions()

x = dim[0] + round(dim[2] / 1.98)
x2 = dim[0] + round(dim[2] / 1.88)
y = dim[1] + round(dim[3] / 2.29)

ex_col = (238, 82, 39)

pyautogui.moveTo(x,y)

while not keyboard.is_pressed('`'):
    t = time.time()
    pixel = getpixel(x, y)
    pixel2 = getpixel(x2, y)

    if get_max_pixel_diff(pixel, ex_col) < 5 or get_max_pixel_diff(pixel2, ex_col) < 5:
        keyboard.press('c')
        time.sleep(1/60)
        keyboard.release('c')

    