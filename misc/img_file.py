#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
import platform
import os

def generateImg(content, filename, driver):
    if('Windows' in platform.system()):
        f = open( filename + ".htm", 'w' )
        f.write( content )
        f.close()

        driver.get(filename + ".htm")
    else:
        driver.get("about:blank")
        driver.delete_all_cookies()
        driver.get("data:text/html;charset=utf-8," + content)
    
    driver.save_screenshot(filename + ".png")
    screen = driver.get_screenshot_as_png()

    box = (0, 0, 320, 240)
    im = Image.open(filename + ".png")
    rgb_im = im.convert('RGB')
    region = rgb_im.crop(box)

    quality = 50
    if("logo" in filename):
        quality = 85
    elif("music" in filename):
        quality = 60
    
    region.save(filename + ".jpg", 'JPEG', optimize=True, quality=quality)
    if(os.path.isfile(filename + ".png")):
        os.remove(filename + ".png")
    if(os.path.isfile(filename + ".htm")):
        os.remove(filename + ".htm")