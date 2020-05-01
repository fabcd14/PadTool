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

from xml.etree import cElementTree as ET
from collections import defaultdict

from misc import str_tools

# Parsing xml file

def parseXml(file,tmpl):
    artist = ""
    title  = ""
    cover  = ""

    xmlf = ET.XML(file)
    xmlt = ET.XML(tmpl)

    # Init temporary work values for listing xml values

    idxLine   = 0
    idxArtist = idxTitle = idxCover = -1

    # Identification of where are the $artist, the $title and the $cover tags are in the tmpl file

    for v in xmlt.iter():
        if(v.text == "$artist"):
            idxArtist = idxLine
        elif(v.text == "$title"):
            idxTitle = idxLine
        elif(v.text == "$cover"):
            idxCover = idxLine
        if(idxArtist != -1 and idxTitle != -1 and idxCover != -1):
            break
        idxLine = idxLine + 1

    # Retrieving info from the xml file with the help of the template file

    idxLine = 0
    for v in xmlf.iter():
        if(idxLine == idxArtist):
            artist = v.text
            str_tools.printMsg ("XML ", "Found artist tag, item nb '" + str(idxLine) + "' with value : '" + artist + "'")
        elif(idxLine == idxTitle):
            title = v.text
            str_tools.printMsg ("XML ", "Found title tag, item nb '" + str(idxLine) + "' with value : '" + title + "'")
        elif(idxLine == idxCover):
            cover = v.text
            str_tools.printMsg ("XML ", "Found cover tag, item nb '" + str(idxLine) + "' with value : '" + cover + "'")
        if(artist != "" and title != "" and cover != ""):
            break
        idxLine = idxLine + 1   

    if(artist == "" or title == "" or cover == ""):
        str_tools.printMsg("XML ", "The following items aren't found :")
        if(artist == ""):
            str_tools.printMsg("XML ", "$artist, ")
        if(title == ""):
            str_tools.printMsg("XML ", "$title, ")
        if(cover == ""):
            str_tools.printMsg("XML ", "$cover")
    return artist, title, cover