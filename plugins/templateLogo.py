#!/usr/bin/python3

from urllib import *
from urllib.request import *
import io
import imgkit
import platform

from misc import img_file
from misc import str_tools

def generate(cfg, driver):
    # Parameters to generate SLS from the config file
    try:
        logo = cfg.get('general', 'logoUrl')
        colorl = cfg.get('general', 'colorl')
        outFolder = cfg.get('general', 'outFolder')
    except configparser.NoOptionError as error:
        str_tools.printMsg("Logo", "Mandatory parameter is missing : " + str(error))
        sys.exit(2)

    str_tools.printMsg ("Logo", "Generating Slide...")

    # Data masking replacement with correct values
    content = ""
    with io.open('themes/logo.html', 'r', encoding="utf-8") as f:
        content = f.read()

    content = content.replace("$logo", logo)
    content = content.replace("$colorl", colorl)

    try: 
        img_file.generateImg(content, outFolder + "/logo", driver)
        str_tools.printMsg ("Logo", "Slide generated at : '" + outFolder + "/logo.jpg'")
    except Exception as ex:
        str_tools.printMsg ("Logo", "Slide generation error : " + str(ex))