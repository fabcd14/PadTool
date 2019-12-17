#!/usr/bin/python3
# -*- coding: utf-8 -*-

version = "v0.7.3"

#Import system libraries
import configparser
from selenium import webdriver
import re
import subprocess
import platform
import time
import sys
import getopt
import os
import threading

from urllib.request import *

driver = None

def header():
    print ("PadTool " + version + " - MOT SLS and DLS generator for PAD encoder")
    print (" By Fabien Cuny (fabcd14) - DAB Radio Normandie")
    print (" ")
    print (" Reads json / xml / txt / html data from a specific file, and outputs DLS+ text")
    print (" from these informations and generates nice SLS with personnalized templates")
    print (" https://github.com/fabcd14")
    print (" ")
    print ("-------------------------------------------------------------------------------")
    print (" ")

def main(argv):
    #Import Plugins
    from plugins import templateATC
    from plugins import templateLogo

    header()

    inputFile = ''
    try:
        opts, args = getopt.getopt(argv,"c:",["config="])
    except getopt.GetoptError:
        print ('padtool.py -c <configfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('padtool.py -c <configfile>')
            sys.exit()
        elif opt in ("-c", "--config"):
            inputFile = arg
    
    if(inputFile == ""):
        print ('Using local config.ini file')
        inputFile = "config.ini"
    else:
        print ('Using config file : "' + inputFile + '"')

    try:
        with open(inputFile): pass
    except IOError:
        print ('The file "' +  inputFile + '" has not been found !')
        sys.exit(2)

    # Config file parsing
    cfg = configparser.ConfigParser()
    cfg.read(inputFile, encoding='utf-8')
    try:
        mode = cfg.get('general', 'mode')
        outFolder = cfg.get('general', 'outFolder')
        radioName = cfg.get('general', 'radioName')
        slogan = cfg.get('general', 'slogan')
    except configparser.NoOptionError as error:
        print("Mandatory parameter is missing : " + str(error))
        sys.exit(2)

    if (mode == 'standalone'):
        try:
            timer = cfg.get('general', 'timer')
            print ("Standalone Mode, timer period set to: " + timer + "s")
        except configparser.NoOptionError as error:
            print("Mandatory parameter is missing: " + str(error))
            sys.exit(2)
    elif (mode == 'server'):
        print ("Server mode")
    else:
        print("Parameter 'mode' not recognized. Only the options 'standalone' or 'server' are supported")
        sys.exit(2)

    # For Proxy
    if int(cfg.get('proxy', 'enabled')) == 1:   
        proxy_handler = ProxyHandler({'http': cfg.get('proxy', 'http'), 'https': cfg.get('proxy', 'https')})
        opener = build_opener(proxy_handler)
        install_opener(opener)

    # Webdriver Init
    print ("[Wdv ] Initializing WebDriver...")
    try:
        driver = webdriver.PhantomJS(service_args=["--disk-cache=false", "--ignore-ssl-errors=true", "--ssl-protocol=any"])
        driver.set_window_size(320, 240)
        print ("[Wdv ] WebDriver Initialized")
    except Exception as error:
        print ("[Wdv ] WebDriver initialization error : " + str(error))

    # Generate slides with logo first if enabled
    try:
        if(cfg.get('slides', 'logo') == "1"):
            templateLogo.generate(cfg, driver)

        title = None
        artist = None

        showName = None
        while True:
            #Generating artist/title/cover slide (with DLS+ if selected)
            if(cfg.get('slides', 'music') == "1"):
                artist, title = templateATC.generate(cfg, driver, artist, title)
            time.sleep(int(timer))
    except configparser.NoOptionError as error:
        print("Mandatory parameter is missing : " + str(error))
        sys.exit(2)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Ctrl+C received : PadTool exits...')
        try:
            sys.exit(0)
            driver = None
        except SystemExit:
            os._exit(0)
            driver = None
    # except Exception as ex:
    #     try:
    #         print ("Error : " + str(ex))
    #         sys.exit(0)
    #     except SystemExit:
    #         os._exit(0)