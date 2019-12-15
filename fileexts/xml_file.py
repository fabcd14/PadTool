#!/usr/bin/python3

from xml.etree import cElementTree as ET
from collections import defaultdict

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
            print ("[XML] Found artist tag, item nb '" + str(idxLine) + "' with value : '" + artist + "'")
        elif(idxLine == idxTitle):
            title = v.text
            print ("[XML] Found title tag, item nb '" + str(idxLine) + "' with value : '" + title + "'")
        elif(idxLine == idxCover):
            cover = v.text
            print ("[XML] Found cover tag, item nb '" + str(idxLine) + "' with value : '" + cover + "'")
        if(artist != "" and title != "" and cover != ""):
            break
        idxLine = idxLine + 1   

    if(artist == "" or title == "" or cover == ""):
        print("[XML] The following items aren't found :")
        if(artist == ""):
            print("[XML] $artist, ")
        if(title == ""):
            print("[XML] $title, ")
        if(cover == ""):
            print("[XML] $cover")
    return artist, title, cover