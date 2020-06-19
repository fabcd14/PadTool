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
import glob
import shutil
import sys
import requests

# Import default Plugins
from plugins import templateATC
from plugins import templateLogo

# Import misc
from misc import str_tools
from misc import server

# Import other Plugins
try:
    from plugins import _pluginsManagement1h
except:
    pass
try:
    from plugins import _pluginsManagement30min
except:
    pass
try:
    from plugins import _pluginsManagement15min
except:
    pass
try:
    from plugins import _pluginsManagement10min
except:
    pass
try:
    from plugins import _pluginsManagement5min
except:
    pass

def initPlugins(pathCfg, cfg, mode, timer):
    title = None
    artist = None

    # Server Mode (or server enabled)
    try:
        port = cfg.get("server", "port")
        user = cfg.get("server", "user")
        password = cfg.get("server", "password")

        if(mode == "server" or port != ""):
            webServer = server.Server(cfg, port, user, password)
            webServer.start()
        str_tools.printMsg("Web ", "PadTool HTTP Server enabled, listening on port " + str(port))
    except:
        pass

    # Standalone Mode Management
    if(cfg.get('slides', 'logo') == "1"):
        templateLogo.generate(cfg)
    time.sleep(1)

    # Regular execution
    totalTime = 0

    triggerHour = True
    triggerQuarterHour = True
    triggerHalfHour = True
    triggerTenMin = True
    triggerFiveMin = True

    listFilesDabCtlSls = []
    listFilesDabCtlDls = []
    indexSlsDabCtlLoop = 0
    indexDlsDabCtlLoop = 0

    while True:
        # Generating artist/title/cover slide (with DLS+ if selected) if mode is not "server"
        if(cfg.get('slides', 'music') == "1" and mode != "server"):
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
            except Exception as ex:
                pass
        if(totalTime == 0 or triggerFiveMin == True):
            triggerFiveMin = False
            try:
                # print("Trigger five minutes")
                _pluginsManagement5min.generate( os.path.abspath(pathCfg) )
            except:
                pass

        # DAB-CTL mode, call at first start when all slides are generated
        if((mode == "dabctl" or mode == 'dabctl-ext') and totalTime == 0):
            try:
                outFolder = cfg.get('general', 'outFolder')
            except configparser.NoOptionError as error:
                str_tools.printMsg("Ext ", "Mandatory parameter is missing : " + str(error))
                sys.exit(2)

            if(mode == 'dabctl'):
                tempFolder = "/tmp/PadTool-" + str(os.getpid())
            elif(mode == "dabctl-ext"):
                tempFolder = outFolder

            try:
                if(os.path.isdir(tempFolder)):
                    listFilesDabCtlSls = [os.path.basename(x) for x in glob.glob(tempFolder + '/*.jpg')]
                    listFilesDabCtlDls = [os.path.basename(x) for x in glob.glob(tempFolder + '/*.txt')]
            except:
                str_tools.printMsg("Ext ", "Mandatory parameter is missing : " + str(error))
                sys.exit(2)

        # DAB-CTL, call each time in loop
        if(mode == "dabctl" or mode == "dabctl-ext"):
            try:
                if (len(listFilesDabCtlSls) != len(glob.glob(tempFolder + '/*.jpg'))):
                    listFilesDabCtlSls = [os.path.basename(x) for x in glob.glob(tempFolder + '/*.jpg')]
            except:
                pass
            try:
                if (len(listFilesDabCtlDls != len(glob.glob(tempFolder + '/*.txt')))):
                    listFilesDabCtlDls = [os.path.basename(x) for x in glob.glob(tempFolder + '/*.txt')]
            except:
                pass

            # Copy SLS
            if(mode == "dabctl"):
                outFolderFilesCount = -1
                timeoutCount = 0
                while(outFolderFilesCount != 0): # Is the folder empty of jpgs ? If then, we push an image.
                    try:
                        outFolderFilesCount = len(glob.glob(outFolder + '/*.jpg'))
                        # print("SLS directory not empty, waiting...")
                    except:
                        outFolderFilesCount = 0
                        # print("SLS directory empty, copying...")
                    time.sleep(1)
                    timeoutCount = timeoutCount + 1
                    if(timeoutCount >= 30):
                        # print("Timeout 30s !")
                        outFolderFilesCount = 0

            try:
                if(len(listFilesDabCtlSls) > 0):
                    # print ("Copy SLS index " + str(indexSlsDabCtlLoop) + " on " + str(len(listFilesDabCtlSls)))
                    if(mode == "dabctl"):
                        shutil.copyfile(tempFolder + '/' + listFilesDabCtlSls[indexSlsDabCtlLoop], outFolder + '/' + os.path.basename(listFilesDabCtlSls[indexSlsDabCtlLoop]))
                    elif(mode == "dabctl-ext"):
                        dabctlExtSend(cfg, "SLS", outFolder + '/' + os.path.basename(listFilesDabCtlSls[indexSlsDabCtlLoop]))
            except Exception as ex:
                pass

            # Copy DLS
            try:
                if(len(listFilesDabCtlDls) > 0):
                    # print ("Copy DLS index " + str(indexDlsDabCtlLoop) + " on " + str(len(listFilesDabCtlDls)))
                    if(mode == "dabctl"):
                        try:
                            outFile = cfg.get('dls', 'outFile')
                        except:
                            str_tools.printMsg("Ext ", "Mandatory parameter is missing : " + str(error))
                            sys.exit(2)
                        
                        shutil.copyfile(tempFolder + '/' + listFilesDabCtlDls[indexDlsDabCtlLoop], outFile)
                    elif(mode == "dabctl-ext"):
                        dabctlExtSend(cfg, "DLS", outFolder + '/' + os.path.basename(listFilesDabCtlDls[indexDlsDabCtlLoop]))
            except Exception as ex:
                pass

            indexSlsDabCtlLoop = indexSlsDabCtlLoop + 1
            indexDlsDabCtlLoop = indexDlsDabCtlLoop + 1
            if(indexSlsDabCtlLoop >= len(listFilesDabCtlSls)):
                indexSlsDabCtlLoop = 0
            if(indexDlsDabCtlLoop >= len(listFilesDabCtlDls)):
                indexDlsDabCtlLoop = 0


        totalTime = totalTime + int(timer)
        if(totalTime >= 3600):
            totalTime = 1
        time.sleep(int(timer))

def dabctlExtSend(cfg, mode, fileToSend):
    hostname = cfg.get('dabctl-ext', 'hostname')
    port = cfg.get('dabctl-ext', 'port')
    pi = cfg.get('dabctl-ext', 'pi')
    try:
        passkey = cfg.get('dabctl-ext', 'passkey')
    except:
        passkey = ""
    
    url = "http://" + hostname + ":" + str(port) + "/_ext"
    try:
        if(mode == "DLS"):
            dls = ""
            with open(fileToSend,'r') as f:
                dls = f.readlines()[-1]
            args = {'PI': pi, 'key': passkey, 'variable': 'DLS', 'value': dls}
            ret = requests.post(url, data = args)
        elif(mode == "SLS"):
            args = {'PI': pi, 'key': passkey, 'variable': 'SLS'}
            files = {'file': open(fileToSend, 'rb')}
            ret = requests.post(url, data = args, files = files)
    except Exception as ex:
        str_tools.printMsg("Ext ", "Error requesting DAB-CTL Server : " + ex)