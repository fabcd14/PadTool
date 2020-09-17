# Copyright (C) 2020
# Fabien Cuny, fabien.cuny7 at orange.fr
# http://www.github.com/fabcd14/PadTool

# This file is part of PadTool.
# PadTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# PadTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with PadTool.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from io import BytesIO
import platform
import os
import time
import base64
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
        options.add_argument('no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('hide-scrollbars')
        options.add_argument('log-level=2')

        driver = webdriver.Chrome(options=options)
        driver.set_window_size(320, 240)
        str_tools.printMsg ("Wdv ", "WebDriver Initialized")
        return driver
    except Exception as error:
        str_tools.printMsg ("Wdv ", "WebDriver initialization error : " + str(error))
        sys.exit(2)

def generateImg(content, filename):
    driver = driverInit()
    driver.get("about:blank")
    driver.delete_all_cookies()

    encodedBytes = base64.b64encode(content.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")

    driver.get("data:text/html;charset=utf-8;base64," + encodedStr)
    
    delay = 5
    try:
        waitLoading = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'end')))
    except TimeoutException:
        str_tools.printMsg ("Wdv ", "Timeout on slide generation")

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