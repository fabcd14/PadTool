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
    from plugins import _pluginsManagement1h
    from plugins import _pluginsManagement30min
    from plugins import _pluginsManagement15min
    from plugins import _pluginsManagement10min
    from plugins import _pluginsManagement5min
except:
    pass

def initPlugins(pathCfg, cfg, mode, timer):
    title = None
    artist = None  

    # Server Mode
    # TODO: Not implented yet :(
    if(mode == "server"):
        print("TODO: Not implented yet :(")
    
    # Standalone Mode Management
    if(mode == "standalone"):
        if(cfg.get('slides', 'logo') == "1"):
            templateLogo.generate(cfg)
        time.sleep(2)   

    # Regular execution
    totalTime = 0

    triggerHour = True
    triggerQuarterHour = True
    triggerHalfHour = True
    triggerTenMin = True
    triggerFiveMin = True

    while True:
        # DAB-CTL mode (regenerating logo each time)
        if(mode == "dabctl"):
            if(cfg.get('slides', 'logo') == "1"):
                templateLogo.generate(cfg)
            _pluginsManagement1h.generate( os.path.abspath(pathCfg) )
            _pluginsManagement30min.generate( os.path.abspath(pathCfg) )

        # Generating artist/title/cover slide (with DLS+ if selected)
        if(cfg.get('slides', 'music') == "1"):
            artist, title = templateATC.generate(cfg, artist, title, mode)

        # Timer reset at 0 when we get to an a new hour / Trigger 1 hour
        if(datetime.datetime.now().minute == 0 and datetime.datetime.now().second <= int(timer) and triggerHour == False): 
            totalTime = 0
            triggerHour = True
        if(datetime.datetime.now().minute != 0):
            triggerHour = False

        # Trigger 30min
        if(datetime.datetime.now().minute == 30 and datetime.datetime.now().second <= int(timer) and triggerHalfHour == False): 
            triggerHalfHour = True
        if(datetime.datetime.now().minute != 30):
            triggerHalfHour = False

        # Trigger 15min
        if(datetime.datetime.now().minute % 15 == 0 and datetime.datetime.now().second <= int(timer) and triggerQuarterHour == False): 
            triggerQuarterHour = True
        if(datetime.datetime.now().minute % 15 != 0):
            triggerQuarterHour = False

        # Trigger 10min
        if(datetime.datetime.now().minute % 10 == 0 and datetime.datetime.now().second <= int(timer) and triggerTenMin == False): 
            triggerTenMin = True
        if(datetime.datetime.now().minute % 10 != 0):
            triggerTenMin = False

        # Trigger 5min
        if(datetime.datetime.now().minute % 5 == 0 and datetime.datetime.now().second <= int(timer) and triggerFiveMin == False): 
            triggerFiveMin = True
        if(datetime.datetime.now().minute % 5 != 0):
            triggerFiveMin = False

        if(totalTime == 0 or triggerHour == True):
            triggerHour = False
            try:
                # print("Trigger hour")
                _pluginsManagement1h.generate( os.path.abspath(pathCfg) )
                _pluginsManagement30min.generate( os.path.abspath(pathCfg) )
            except:
                pass
        if(totalTime == 0 or triggerHalfHour == True):
            triggerHalfHour = False
            try:
                # print("Trigger half hour")
                _pluginsManagement30min.generate( os.path.abspath(pathCfg) )
            except:
                pass
        if(totalTime == 0 or triggerQuarterHour == True):
            triggerQuarterHour = False
            try:
                # print("Trigger quarter hour")
                _pluginsManagement15min.generate( os.path.abspath(pathCfg) )
            except:
                pass
        if(totalTime == 0 or triggerTenMin == True):
            triggerTenMin = False
            try:
                # print("Trigger ten minutes")
                _pluginsManagement10min.generate( os.path.abspath(pathCfg) )
            except:
                pass
        if(totalTime == 0 or triggerFiveMin == True):
            triggerFiveMin = False
            try:
                # print("Trigger five minutes")
                _pluginsManagement5min.generate( os.path.abspath(pathCfg) )
            except:
                pass  
    
        totalTime = totalTime + int(timer)
        if(totalTime >= 3600):
            totalTime = 1
        
        time.sleep(int(timer))