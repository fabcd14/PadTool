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

from urllib import *
from urllib.request import *
import io
import os
import imgkit
import platform

from misc import img_file
from misc import str_tools

def generate(cfg):
    # Parameters to generate SLS from the config file
    try:
        logo = cfg.get('general', 'logoUrl')
        colorl = cfg.get('general', 'colorl')
        mode = cfg.get('general', 'mode')
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
                    body { margin:auto; background-color:$colorl; background:$colorl;}
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
        if(mode == "dabctl"):
            img_file.generateImg(content, "/tmp/PadTool-" + str(os.getpid()) + "/logo")
            str_tools.printMsg ("Logo", "Slide generated at : '" + "/tmp/PadTool-" + str(os.getpid()) + "/logo.jpg' and will be copied to '" + outFolder + "/logo.jpg'")
        else:
            img_file.generateImg(content, outFolder + "/logo")
            str_tools.printMsg ("Logo", "Slide generated at : '" + outFolder + "/logo.jpg'")
    except Exception as ex:
        str_tools.printMsg ("Logo", "Slide generation error : " + str(ex))