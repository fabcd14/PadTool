#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from io import BytesIO
import platform
import os
import time
import base64

from selenium import webdriver
from PIL import Image

from misc import str_tools

def driverInit():
    driver = None
    str_tools.printMsg ("Wdv ", "Initializing WebDriver...")
    try:
        #Formerly with PhantomJS until v0.8.0
        #driver = webdriver.PhantomJS(service_args=["--disk-cache=false", "--ignore-ssl-errors=true", "--ssl-protocol=any"])
        
        #Now with ChromeDriver since v0.9.0
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('hide-scrollbars')
        options.add_argument('log-level=2')

        driver = webdriver.Chrome(options=options)
        driver.set_window_size(320, 240)
        str_tools.printMsg ("Wdv ", "WebDriver Initialized")
    except Exception as error:
        str_tools.printMsg ("Wdv ", "WebDriver initialization error : " + str(error))
    return driver

def generateImg(content, filename):
    driver = driverInit()
    driver.get("about:blank")
    driver.delete_all_cookies()

    encodedBytes = base64.b64encode(content.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")

    driver.get("data:text/html;charset=utf-8;base64," + encodedStr)
    
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
    driver.quit()