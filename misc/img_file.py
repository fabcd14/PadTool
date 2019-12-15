#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
import platform
import os

from misc import strTools

def generateImg(content, filename, driver):
    content = strTools.parseCharsForImg(content)

    # If path given is relative, we append the current folder
    # if (os.path.isabs(filename) == False):
    #     filename = os.getcwd() + filename

    #f = open( filename + ".htm", 'w' )
    #f.write( content )
    #f.close()

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

    # if("logo" in filename):
    #     region.save("img//logo.jpg", 'JPEG', optimize=True, quality=55)
    # if("music" in filename):
    #     region.save("img//music.jpg", 'JPEG', optimize=True, quality=55)