#!/usr/bin/python3

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

import json

from misc import str_tools

def searchForJson(expr, d, parent=[], level=0):
    found = 0
    if(isinstance(d, dict)):
        for k, v in d.items():
            if(isinstance(v, dict)):
                parent.append(k)
                level = level+1
                parent, level, found = searchForJson(expr, v, parent, level)
                if (found == 1):
                    return parent, level, found
                parent.pop(len(parent)-1)
            elif(isinstance(v, list)):
                parent.append(k)
                level = level+1
                parent, level, found = searchForJson(expr, v, parent, level)
                if (found == 1):
                    return parent, level, found
                parent.pop(len(parent)-1)
            else:
                if (v == expr):
                    parent.append(k)
                    str_tools.printMsg ("JSON", "Tag '" + expr + "' found in : " + str(parent))
                    return parent, level, 1
    if(isinstance(d, list)):
        idx = 0
        for item in d:
            if(isinstance(item, list)):
                parent.append(item)
                level = level+1
                parent, level, found = searchForJson(expr, item, parent, level)
                if (found == 1):
                    return parent, level, found
                parent.pop(len(parent)-1)
            else:
                for k, v in item.items():
                    if(isinstance(v, dict)):
                        parent.append(k)
                        level = level+1
                        parent, level, found = searchForJson(expr, v, parent, level)
                        if (found == 1):
                            return parent, level, found
                        parent.pop(len(parent)-1)
                    elif(isinstance(v, list)):
                        parent.append(k)
                        level = level+1
                        parent, level, found = searchForJson(expr, v, parent, level)
                        if (found == 1):
                            return parent, level, found
                        parent.pop(len(parent)-1)
                    else:
                        if (v == expr):
                            if(d.count != 1):
                                parent.append(idx)
                            parent.append(k)
                            str_tools.printMsg ("JSON", "Tag '" + expr + "' found in : " + str(parent))
                            return parent, level, 1
            idx = idx+1
    return parent, level, found
                
def getTagInCurJson(jsonTags, jsonDict):
    ret = ""
    try:
        if(isinstance(jsonTags[0][0], int)):
            if(jsonTags[0][0] > len(jsonDict)):
                str_tools.printMsg("JSON", "Source file sized differently from template (max: "+ jsonTags[0][0] +"). Parameter changed to max of json source: " + len(jsonDict) -1)
                jsonTags[0][0] = len(jsonDict) -1
    except:
        pass

    for i in range(len(jsonTags[0])):
        r0 = jsonTags[0][i]
        try:
            if(i==0): #First
                ret = jsonDict[r0]
            elif (i == len(jsonTags[0]) - 1): #Last one
                if(isinstance(ret, list)):
                    ret = ret[0][r0]
                else:
                    try:
                        ret = ret[r0]
                    except:
                        ret = ""
            else: #n index in middle
                if(isinstance(ret, list)):
                    ret = ret[0][r0]
                else:
                    try:
                        ret = ret[r0]
                    except:
                        ret = ""
        except:
            pass
    return ret

def parseJson(file,tmpl):
    artist = ""
    title  = ""
    cover  = ""

    try:
        file = file.decode('utf-8')
    except:
        pass
    
    try:
        if (file.index("{") != 0):
            file = file[file.index("{"):]
        while (file[len(file)-1] != "}"):
            file = file[0:-1]
        if (tmpl.index("{") != 0):
            tmpl = tmpl[tmpl.index("{"):]
        while (tmpl[len(tmpl)-1] != "}"):
            tmpl = tmpl[0:-1]
    except:
        pass

   
    # Identification of where are the $artist, the $title and the $cover tags are in the tmpl file
    jsonDecoderTemplate = json.JSONDecoder()

    jsonTemplate = ""
    try:
        jsonTemplate = jsonDecoderTemplate.decode(tmpl)
    except:
        jsonTemplate = jsonDecoderTemplate.decode("[" + tmpl + "]")

    jsonNF  = ""
    try:
        jsonNF = jsonDecoderTemplate.decode(file)
    except:
        jsonNF = jsonDecoderTemplate.decode("[" + file + "]")

    try:
        artist = getTagInCurJson(searchForJson("$artist", jsonTemplate, []),jsonNF)
        title = getTagInCurJson(searchForJson("$title", jsonTemplate, []),jsonNF)
        cover = getTagInCurJson(searchForJson("$cover", jsonTemplate, []),jsonNF)
    except Exception as ex:
        print("Json Parsing Error : " + str(ex))
        artist = ""
        title = ""
        cover = ""

    if(artist == "" or title == "" or cover == ""):
        str_tools.printMsg("JSON" ,"The following items aren't found in the json source file:")
        if(artist == ""):
            str_tools.printMsg("JSON", "$artist, ")
        if(title == ""):
            str_tools.printMsg("JSON", "$title, ")
        if(cover == ""):
            str_tools.printMsg("JSON", "$cover")
    return artist, title, cover
