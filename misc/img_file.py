#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from io import BytesIO
import platform
import os
import time

def generateImg(content, filename, driver):
    driver.get("about:blank")
    driver.delete_all_cookies()
    driver.get("data:text/html;charset=utf-8," + content)
    
    time.sleep(1)

    png = driver.get_screenshot_as_png()

    box = (0, 0, 320, 240)
    im = Image.open(BytesIO(png))
    rgb_im = im.convert('RGB')
    region = rgb_im.crop(box)

    quality = 50
    if("logo" in filename):
        quality = 85
    elif("music" in filename):
        quality = 60
    
    region.save(filename + ".jpg", 'JPEG', optimize=True, quality=quality)