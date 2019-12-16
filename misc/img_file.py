#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
import platform
import os

from misc import strTools

def generateImg(content, filename, driver):
    content = strTools.parseCharsForImg(content)

    with open(filename + ".htm",'wt') as f:
        f.write(content)
    if('Windows' in platform.system()):
        cwd = "file:///" + os.getcwd().replace("\\", "/") + "/" + filename + ".htm"
    else:
        cwd = "file://" + os.getcwd() + "/" + filename + ".htm"

    driver.get(cwd)
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