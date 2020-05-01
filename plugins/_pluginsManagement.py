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
import time
import configparser
import os
import datetime

# Import default Plugins
from plugins import templateATC
from plugins import templateLogo

# Import other Plugins
try:
    from plugins import _hourlyPluginsManagement
    from plugins import _halfHourPluginsManagement
except:
    pass

def initPlugins(pathCfg, cfg, mode, timer):
    title = None
    artist = None

    # Standalone Mode Management
    if(mode == "standalone"):
        if(cfg.get('slides', 'logo') == "1"):
            templateLogo.generate(cfg)
        time.sleep(2)     

    # Server Mode
    # TODO: Not implented yet :(
    
    # Regular execution
    totalTime = 0
    hourResetTriggered = False
    while True:
        # DAB-CTL mode (regenerating logo each time)
        if(mode == "dabctl"):
            if(cfg.get('slides', 'logo') == "1"):
                templateLogo.generate(cfg)
            _hourlyPluginsManagement.generate( os.path.abspath(pathCfg) )
            _halfHourPluginsManagement.generate( os.path.abspath(pathCfg) )

        # Generating artist/title/cover slide (with DLS+ if selected)
        if(cfg.get('slides', 'music') == "1"):
            artist, title = templateATC.generate(cfg, artist, title, mode)

        if(totalTime == 0 or totalTime >= 3600):
            try:
                _hourlyPluginsManagement.generate( os.path.abspath(pathCfg) )
            except:
                pass
        if(totalTime == 0 or (totalTime >= 1800 and totalTime <= (int(timer) + 7))):
            try:
                _halfHourPluginsManagement.generate( os.path.abspath(pathCfg) )
            except:
                pass

        totalTime = totalTime + int(timer) + 5
        if(totalTime >= 3600):
            totalTime = 1
        
        # Timer reset at 0 when we get to an a new hour
        if(datetime.datetime.now().minute == 0 and hourResetTriggered == False): 
            totalTime = 0
            hourResetTriggered = True
        if(datetime.datetime.now().minute != 0):
            hourResetTriggered = False
        
        time.sleep(int(timer))