#!/usr/bin/python3

from urllib import *
from urllib.request import *
from datetime import datetime
import io
import json
import platform
import configparser
import os
import ssl
import html
import time
import sys
import coverpy

from fileexts import json_file
from fileexts import xml_file
from fileexts import txt_file
from misc import img_file
from misc import str_tools

def generate(cfg, lastArtist, lastTitle, mode):
    # Avoid SSL errors
    ssl._create_default_https_context = ssl._create_unverified_context

    # Parameters to generate SLS from the config file
    try: 
        logo = cfg.get('general', 'logoUrl')
        color1 = cfg.get('general', 'color1')
        color2 = cfg.get('general', 'color2')
        backUrl = cfg.get('general', 'backUrl')
        theme = "themes/" + cfg.get('general', 'theme')
        radioName = cfg.get('general', 'radioName')
        slogan = cfg.get('general', 'slogan')
        outFolder = cfg.get('general', 'outFolder')
    except configparser.NoOptionError as error:
        str_tools.printMsg("ATC", "Mandatory parameter is missing : " + str(error))
        sys.exit(2)

    # Opening Template
    file = "" 
    cptFails = 0 # Count connection failures, exits the app when not reached for 5 times.

    # Checking connecion failures
    while True:
        try: 
            file = urlopen(cfg.get('source', 'url')).read()
            cptFails = 0
            break
        except: 
            cptFails = cptFails + 1
            if(cptFails < 5):
                str_tools.printMsg("ATC ", "[" + str(cptFails) + "/5] Failed to open source file. Retrying in 10secs...")
                time.sleep(10)
            else:
                str_tools.printMsg("ATC ", "[" + str(cptFails) + "/5] Failed 5 times to open source file. PadTool will exits...")
                sys.exit(2)
        
    # Parsing formalisms for $artist and $title tags
    artistForm = 0
    titleForm = 0
    try:
        artistForm = cfg.get('general','artistForm')
        if(artistForm == ""): 
            artistForm = 0
    except:
        artistForm = 0
    try:
        titleForm = cfg.get('general','titleForm')
        if(titleForm == ""): 
            titleForm = 0
    except:
        titleForm = 0

    tmpl = ""
    with open(cfg.get('source', 'template'), "r") as template:
        for line in template:
            tmpl = tmpl + line

    ret = []
    if (cfg.get('source','format') == "json"):
        ret = json_file.parseJson(file, tmpl)
    elif (cfg.get('source','format') == "xml"):
        ret = xml_file.parseXml(file,tmpl)
    elif (cfg.get('source','format') == "txt"):
        ret = txt_file.parseTxt(file,tmpl)

    artist = str_tools.formString(str(html.unescape(str(ret[0]))), int(artistForm)).strip()
    title  = str_tools.formString(str(html.unescape(str(ret[1]))), int(titleForm)).strip()
    cover  = html.unescape(str(ret[2]))

    if(artist == lastArtist and title == lastTitle):
        str_tools.printMsg("ATC ", "SLS/DLS already generated, passing...")
        return artist, title

    # Filters management for artist tag
    filterFound = False

    try:
        filterArtist = json.loads(cfg.get('filter', 'artist'))
        str_tools.printMsg("ATC ", "Filters defined for artist tag")

        for fart in filterArtist:
            if (str(fart) == artist):
                filterFound = True
                str_tools.printMsg ("ATC ", "Filter '" + str(fart) +"' found in artist tag")
                if(os.path.isfile(outFolder + "/music.jpg")):
                    os.remove(outFolder + "/music.jpg")
                    str_tools.printMsg ("ATC ", "SLS exists, deleting slide...")
                    # Create file REQUEST_SLIDES_DIR_REREAD
                    f = open( outFolder + '/REQUEST_SLIDES_DIR_REREAD', 'w' )
                    f.write("")
                    f.close()  
    except configparser.NoOptionError as error:
        str_tools.printMsg("ATC ", "No filters defined for artist tag, ignoring...")
    except configparser.NoSectionError as error:
        str_tools.printMsg("ATC ", "No filters defined for artist tag, ignoring...")
    except json.decoder.JSONDecodeError as ex:
        str_tools.printMsg("ATC ", "No filters defined for artist tag (bad format or empty), ignoring...")

    # Filters management for title tag
    try:
        filterTitle = json.loads(cfg.get('filter', 'title'))
        str_tools.printMsg("ATC ", "Filters defined for title tag")

        for ftit in filterTitle:
            if (str(ftit) == title):
                filterFound = True
                str_tools.printMsg ("ATC ", "Filter '" + str(ftit) + "' found in title tag")
                if(os.path.isfile(outFolder + "/music.jpg")):
                    str_tools.printMsg ("ATC ", "SLS exists, deleting slide...")
                    os.remove(outFolder + "/music.jpg")
                    # Create file REQUEST_SLIDES_DIR_REREAD
                    f = open( outFolder + '/REQUEST_SLIDES_DIR_REREAD', 'w' )
                    f.write("")
                    f.close() 
                break
    except configparser.NoOptionError as error:
        str_tools.printMsg("ATC ", "No filters defined for title tag, ignoring...")
    except configparser.NoSectionError as error:
        str_tools.printMsg("ATC ", "No filters defined for title tag, ignoring...")
    except json.decoder.JSONDecodeError as ex:
        str_tools.printMsg("ATC ", "No filters defined for title tag (bad format or empty), ignoring...")

    # Find the cover on CoverPy
    coverPyEnabled = "0"
    coverPyFound = False

    try:
        coverPyEnabled = cfg.get('source', 'researchCover')
    except:
        pass

    if not cover and coverPyEnabled == "1":
        cpy = coverpy.CoverPy()
        try:
            str_tools.printMsg ("ATC ", "No cover URL provided, using CoverPy to find one cover...")
            result = cpy.get_cover(artist + " - " + title, 1)
            cover = result.artwork(300)
            coverPyFound = True
            str_tools.printMsg ("ATC ", "Cover found using CoverPy : " + cover)
        except coverpy.exceptions.NoResultsException:
            str_tools.printMsg ("ATC ", "No cover found using CoverPy")
        except:
            str_tools.printMsg ("ATC ", "Error with CoverPy")

    # Put default cover when no cover image provided (eg. logo of the radio station)
    if (not cover and coverPyFound == False) or filterFound == True:
        str_tools.printMsg ("ATC ", "Putting default cover as no URL has been provided or if a filter has been found")
        try:
            cover = cfg.get('source','defaultCover')
        except configparser.NoOptionError as error:
            str_tools.printMsg("ATC ", "Mandatory parameter is missing : " + str(error))
            sys.exit(2)

    tempArtist = str(lastArtist).replace("...", "")
    tempTitle = str(lastTitle).replace("...", "")

    # Some APIs do not use http or https prefix, add http:// when it's the case
    if (len(cover) > 0):
        if("http" not in cover):
            cover = str(cfg.get('general', 'prefix')) + cover
            if(filterFound == True or (artist == "" and title == "")):
                try:
                    contentDls = cfg.get('dls', 'defaultDls')
                except:
                    contentDls = "$radioName, $slogan"
                if(os.path.isfile(outFolder + "/music.jpg")):
                    os.remove(outFolder + "/music.jpg")
            else:
                contentDls = cfg.get('dls', 'text')

    # Data masking replacement with correct values
    content = ""
    with io.open(theme + '.html', 'r', encoding="utf-8") as f:
        content = f.read()

    if (cfg.get('dls','enabled') == "1"):
        if((artist not in tempArtist and title not in tempTitle) or (artist == "" and title == "")):
            str_tools.printMsg ("ATC ", "Generating DLS...")
            if(filterFound == True or (artist == "" and title == "")):
                try:
                    contentDls = cfg.get('dls', 'defaultDls')
                except:
                    contentDls = "$radioName, $slogan"
                if(os.path.isfile(outFolder + "/music.jpg")):
                    os.remove(outFolder + "/music.jpg")
            else:
                contentDls = cfg.get('dls', 'text')

            lenDls       = len(contentDls)
            lenArtist    = len(str(artist))
            lenTitle     = len(str(title))
            lenRadioName = len(radioName)

            contentDls = contentDls.replace("$artist", artist)
            contentDls = contentDls.replace("$title", title)
            contentDls = contentDls.replace("$radioName", radioName)
            contentDls = contentDls.replace("$slogan", slogan)

            idxArtist    = -1
            idxTitle     = -1
            idxRadioName = -1

            if (artist in contentDls and artist != ""):
                idxArtist = contentDls.index(artist)
            if (title in contentDls and title != ""):
                idxTitle = contentDls.index(title)
            if (radioName in contentDls and radioName != ""):
                idxRadioName = contentDls.index(radioName)

            dlsPlusEnabled = "0"
            try:
                # Parsing option in the config file if the DLS+ is enabled or not.
                if(cfg.get('dls', 'dlsPlus') != ""):
                    dlsPlusEnabled = cfg.get('dls', 'dlsPlus')
            except:
                dlsPlusEnabled = "0"

            if(dlsPlusEnabled == "1"):    
                dlPlus = "##### parameters { #####\nDL_PLUS=1\nDL_PLUS_ITEM_TOGGLE=0\nDL_PLUS_ITEM_RUNNING=1\n"
                
                if (idxRadioName != -1):
                    dlPlus = dlPlus + "DL_PLUS_TAG=32 " + str(idxRadioName) + " " + str(lenRadioName -1) + "\n"
                if (idxTitle != -1):
                    dlPlus = dlPlus + "DL_PLUS_TAG=1 " + str(idxTitle) + " " + str(lenTitle - 1) + "\n"
                if (idxArtist != -1):
                    dlPlus = dlPlus + "DL_PLUS_TAG=4 " + str(idxArtist) + " " + str(lenArtist - 1) + "\n"
                dlPlus = dlPlus + "##### parameters } #####"
            outDls = outFolder + '/dls.txt'
            try:
                # Parsing option in the config file if the DLS file should be generated in an other path.
                if(cfg.get('dls', 'outFile') != ""):
                    outDls = cfg.get('dls', 'outFile') 
            except:
                pass
            f = open(outDls, 'w')
            if(dlsPlusEnabled == "1"):   
                f.write(dlPlus + "\n" + contentDls)
            else:
                f.write(contentDls)
            f.close()

            try:
                if(cfg.get('dls', 'outFile') != ""):
                    if(dlsPlusEnabled == "1"):
                        str_tools.printMsg ("ATC ", "DLS exported with DLS+ : '" + contentDls + "' at '" + outDls + "'")
                    else:
                        str_tools.printMsg ("ATC ", "DLS exported : '" + contentDls + "' at '" + outDls + "'")
            except:
                if(dlsPlusEnabled == "1"):   
                    str_tools.printMsg ("ATC ", "DLS exported with DLS+ : '" + contentDls + "' at '" + outFolder + "/dls.txt'")
                else:
                    str_tools.printMsg ("ATC ", "DLS exported : '" + contentDls + "' at '" + outDls + "'")

    # If a filter has been found, we don't generate any artist, title slide
    if(filterFound == True):
        return artist, title

    # If a there is no artist nor title, we don't generate any artist, title slide
    if(artist == "" or title == ""):
        return artist, title

    # If title and/or artist are too long to be displayed on a slide, we reduce them
    if(len(str(artist)) > 35):
        artist = str(artist)[0:35] + "..."
    if(len(str(title)) > 35):
        title = str(title)[0:35] + "..."

    if(mode != "dabctl"):
        if(artist == lastArtist and title == lastTitle):
            str_tools.printMsg("ATC ", "SLS/DLS already generated, passing...")
            return artist, title

    str_tools.printMsg ("ATC ", "Generating Slide...")

    # content = content.replace("$artist", str(artist.encode("utf-8").decode('unicode_escape')))
    # content = content.replace("$title", str(title.encode("utf-8").decode('unicode_escape')))
    content = content.replace("$artist", str_tools.formString(str(artist), int(artistForm)).strip())
    content = content.replace("$title", str_tools.formString(str(title), int(titleForm)).strip())
    content = content.replace("$color1", color1)
    content = content.replace("$color2", color2)
    content = content.replace("$backurl", backUrl)
    content = content.replace("$logo", logo)
    try:
        respCover = urlopen(cover).getcode()
    except:
        cover = cfg.get('source','defaultCover')
    content = content.replace("$cover", cover)

    try:     
        img_file.generateImg(content, outFolder + "/music")
        str_tools.printMsg ("ATC ", "Slide generated at : '" + outFolder + "/music.jpg'")
    except Exception as ex:
        str_tools.printMsg ("ATC ", "Slide generation error : " + str(ex))
    
    # Create file REQUEST_SLIDES_DIR_REREAD
    f = open(outFolder + '/REQUEST_SLIDES_DIR_REREAD', 'w' )
    f.write("")
    f.close()  

    return artist, title