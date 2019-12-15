#!/usr/bin/python3

import json

def iterate_all(iterable, returned="key"):
    
    """Returns an iterator that returns all keys or values
       of a (nested) iterable.
       
       Arguments:
           - iterable: <list> or <dictionary>
           - returned: <string> "key" or "value"
           
       Returns:
           - <iterator>
    """
  
    if isinstance(iterable, dict):
        for key, value in iterable.items():
            if returned == "key":
                yield key
            elif returned == "value":
                if not (isinstance(value, dict) or isinstance(value, list)):
                    yield value
            else:
                raise ValueError("'returned' keyword only accepts 'key' or 'value'.")
            for ret in iterate_all(value, returned=returned):
                yield ret
    elif isinstance(iterable, list):
        for el in iterable:
            for ret in iterate_all(el, returned=returned):
                yield ret

def parseJson(file,tmpl):
    artist = ""
    title  = ""
    cover  = ""


    file = file.decode('utf-8')
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
    
    try:
        jsnf = json.loads(file)
    except: 
        jsnf = json.loads("[" + file + "]")
        
    try:
        jstp = json.loads(tmpl)
    except: 
        jstp = json.loads("[" + tmpl + "]")

    # Init temporary work values for listing json values

    idxLine   = 0
    idxArtist = idxTitle = idxCover = -1

    # Identification of where are the $artist, the $title and the $cover tags are in the tmpl file

    for v in iterate_all(jstp, "value"):
        if(v == "$artist"):
            idxArtist = idxLine
        elif(v == "$title"):
            idxTitle = idxLine
        elif(v == "$cover"):
            idxCover = idxLine
        if(idxArtist != -1 and idxTitle != -1 and idxCover != -1):
            break
        idxLine = idxLine + 1

    # Retrieving info from the json file with the help of the template file

    idxLine = 0
    for v in iterate_all(jsnf, "value"):
        if(idxLine == idxArtist):
            if(v != None):
                artist = v
                print ("[JSON] Found artist tag, item nb '" + str(idxLine) + "' with value : '" + str(artist) + "'")
        elif(idxLine == idxTitle):
            if(v != None):
                title = v
                print ("[JSON] Found title tag, item nb '" + str(idxLine) + "' with value : '" + str(title) + "'")
        elif(idxLine == idxCover):
            if(v != None):
                cover = v
                print ("[JSON] Found cover tag, item nb '" + str(idxLine) + "' with value : '" + str(cover) + "'")
        if(artist != "" and title != "" and cover != ""):
            break
        idxLine = idxLine + 1   

    if(artist == "" or title == "" or cover == ""):
        print("[JSON] The following items aren't found :")
        if(artist == ""):
            print("[JSON] $artist, ")
        if(title == ""):
            print("[JSON] $title, ")
        if(cover == ""):
            print("[JSON] $cover")
    return artist, title, cover
