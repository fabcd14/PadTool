#!/usr/bin/python3

from urllib import *
from urllib.request import *
import io
import imgkit
import platform

from misc import img_file
from misc import str_tools

def generate(cfg):
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
    content = """
        <html>
            <head>
                <style type="text/css">
                    body { margin:auto; background-color:$colorl; }
                    .conteneur{ width: 315px; height: 235px; text-align: center; display: table-cell; vertical-align: middle; }
                    img { max-width: 300px; max-height: 220px; }
                </style>
            </head>
            
            <body> <div class="conteneur"> <img src="$logo" /> </div> </body>
        </html>
    """

    content = content.replace("$logo", logo)
    content = content.replace("$colorl", colorl)

    try: 
        img_file.generateImg(content, outFolder + "/logo")
        str_tools.printMsg ("Logo", "Slide generated at : '" + outFolder + "/logo.jpg'")
    except Exception as ex:
        str_tools.printMsg ("Logo", "Slide generation error : " + str(ex))