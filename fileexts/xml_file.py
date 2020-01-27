#!/usr/bin/python3

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