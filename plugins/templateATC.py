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

from fileexts import json_file
from fileexts import xml_file
from fileexts import txt_file
from misc import img_file

from selenium import webdriver
from PIL import Image

def generate(cfg, driver, lastArtist, lastTitle):
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
        print("[ATC ] Mandatory parameter is missing : " + str(error))
        sys.exit(2)

    # Opening Template
    file = urlopen(cfg.get('source', 'url')).read()
    tmpl = ""

    with open (cfg.get('source', 'template'), "r") as template:
        for line in template:
            tmpl = tmpl + line

    ret = []
    if (cfg.get('source','format') == "json"):
        ret = json_file.parseJson(file, tmpl)
    elif (cfg.get('source','format') == "xml"):
        ret = xml_file.parseXml(file,tmpl)
    elif (cfg.get('source','format') == "txt"):
        ret = txt_file.parseTxt(file,tmpl)

    artist = html.unescape(str(ret[0]))
    title  = html.unescape(str(ret[1]))
    cover  = html.unescape(str(ret[2]))

    # Filters management for artist tag
    filterFound = False

    try:
        filterArtist = json.loads(cfg.get('filter', 'artist'))
        print("[ATC ] Filters defined for artist tag")

        for fart in filterArtist:
            if (str(fart) == artist):
                filterFound = True
                print ("[ATC ] Filter '" + str(fart) +"' found in artist tag")
                if(os.path.isfile(outFolder + "/music.jpg")):
                    os.remove(outFolder + "/music.jpg")
                    print ("[ATC ] SLS exists, deleting slide...")
                    # Create file REQUEST_SLIDES_DIR_REREAD
                    f = open( outFolder + '/REQUEST_SLIDES_DIR_REREAD', 'w' )
                    f.write("")
                    f.close()  
    except configparser.NoOptionError as error:
        print("[ATC ] No filters defined for artist tag, ignoring...")
    except configparser.NoSectionError as error:
        print("[ATC ] No filters defined for artist tag, ignoring...")
    except json.decoder.JSONDecodeError as ex:
        print("[ATC ] No filters defined for artist tag (bad format or empty), ignoring...")

    # Filters management for title tag
    try:
        filterTitle = json.loads(cfg.get('filter', 'title'))
        print("[ATC ] Filters defined for title tag")

        for ftit in filterTitle:
            if (str(ftit) == title):
                filterFound = True
                print ("[ATC ] Filter '" + str(ftit) + "' found in title tag")
                if(os.path.isfile(outFolder + "/music.jpg")):
                    print ("[ATC ] SLS exists, deleting slide...")
                    os.remove(outFolder + "/music.jpg")
                    # Create file REQUEST_SLIDES_DIR_REREAD
                    f = open( outFolder + '/REQUEST_SLIDES_DIR_REREAD', 'w' )
                    f.write("")
                    f.close() 
                break
    except configparser.NoOptionError as error:
        print("[ATC ] No filters defined for title tag, ignoring...")
    except configparser.NoSectionError as error:
        print("[ATC ] No filters defined for title tag, ignoring...")
    except json.decoder.JSONDecodeError as ex:
        print("[ATC ] No filters defined for title tag (bad format or empty), ignoring...")

    if(artist == lastArtist and title == lastTitle):
        print("[ATC ] SLS/DLS already generated, passing...")
        return artist, title

    # Put default cover when no cover image provided (eg. logo of the radio station)
    if not cover or filterFound == True:
        print ("[ATC ] Putting default cover as no URL has been provided")
        try:
            cover = cfg.get('source','defaultCover')
        except configparser.NoOptionError as error:
            print("[ATC ] Mandatory parameter is missing : " + str(error))
            sys.exit(2)

    # Some APIs do not use http or https prefix, add http:// when it's the case
    if (len(cover) > 0):
        if("http" not in cover):
            cover = str(cfg.get('general', 'prefix')) + cover

    # Data masking replacement with correct values
    content = ""
    with io.open(theme + '.html', 'r', encoding="utf-8") as f:
        content = f.read()

    if (cfg.get('dls','enabled') == "1"):
        print ("[ATC ] Generating DLS...")
        if(filterFound == True or (artist == "" and title == "")):
            contentDls = "$radioName, $slogan"
        else:
            contentDls = cfg.get('dls', 'text')

        lenDls       = len(contentDls)
        lenArtist    = len(str(artist))
        lenTitle     = len(str(title))
        lenRadioName = len(radioName)

        contentDls = contentDls.replace("$artist", str(artist))
        contentDls = contentDls.replace("$title", str(title))
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

        dlPlus = "##### parameters { #####\nDL_PLUS=1\nDL_PLUS_ITEM_TOGGLE=0\nDL_PLUS_ITEM_RUNNING=1\n"
        
        if (idxRadioName != -1):
            dlPlus = dlPlus + "DL_PLUS_TAG=32 " + str(idxRadioName) + " " + str(lenRadioName -1) + "\n"
        if (idxTitle != -1):
            dlPlus = dlPlus + "DL_PLUS_TAG=1 " + str(idxTitle) + " " + str(lenTitle - 1) + "\n"
        if (idxArtist != -1):
            dlPlus = dlPlus + "DL_PLUS_TAG=4 " + str(idxArtist) + " " + str(lenArtist - 1) + "\n"
        dlPlus = dlPlus + "##### parameters } #####"
        f = open( outFolder + '/dls.txt', 'w' )
        f.write( dlPlus + "\n" + contentDls )
        f.close()

        print ("[ATC ] DLS exported with DLS+ : '" + contentDls + "' at '" + outFolder + "/dls.txt'")

    # If a filter has been found, we don't generate any artist, title slide
    if(filterFound == True):
        return artist, title

    # If a there is no artist nor title, we don't generate any artist, title slide
    if(artist == "" or title == ""):
        return artist, title

    if(len(str(artist)) > 35):
        artist = str(artist)[0:35] + "..."
    if(len(str(title)) > 35):
        title = str(title)[0:35] + "..."

    content = content.replace("$artist", str(artist))
    content = content.replace("$title", str(title))
    content = content.replace("$color1", color1)
    content = content.replace("$color2", color2)

    print ("[ATC ] Generating Slide...")

    if(int(cfg.get('proxy', 'enabled')) == 1):
        if('Windows' in platform.system()):
            tempPathLogo  = "C://Temp//logo.jpg"
            tempPathCover = "C://Temp//cover.jpg"
            tempPathBack  = "C://Temp//backurl.jpg"
            tempUrlLogo   = "file:///C:/Temp/logo.jpg"
            tempUrlCover  = "file:///C:/Temp/cover.jpg?t=" + str(datetime.timestamp(datetime.now()))
            tempUrlBack   = "file:///C:/Temp/backurl.jpg"
        else:
            tempPathLogo  = "/tmp/logo.jpg"
            tempPathCover = "/tmp/cover.jpg"
            tempPathBack  = "/tmp/backurl.jpg"
            tempUrlLogo   = "file:///tmp/logo.jpg"
            tempUrlCover  = "file:///tmp/cover.jpg?t=" + str(datetime.timestamp(datetime.now()))
            if (backUrl != ""):
                tempUrlBack   = "file:///tmp/backurl.jpg"

        urlretrieve(logo, tempPathLogo)
        try:
            urlretrieve(cover, tempPathCover)
        except:
            print("[ATC ] HTTP Error, putting default cover...")
            cover = cfg.get('source','defaultCover')
            urlretrieve(cover, tempPathCover)
        if (backUrl != ""):
            urlretrieve(backUrl, tempPathBack)
        content = content.replace("$logo", tempUrlLogo)
        content = content.replace("$cover", tempUrlCover)
        if (backUrl != ""):
            content = content.replace("$backurl", tempUrlBack)
    else:
        content = content.replace("$backurl", backUrl)
        content = content.replace("$logo", logo)
        content = content.replace("$cover", cover)

    try:     
        img_file.generateImg(content, outFolder + "/music", driver)
        print ("[ATC ] Slide generated at : '" + outFolder + "/music.jpg'")
    except Exception as ex:
        print ("[ATC ] Slide generation error : " + str(ex))
    
    # Create file REQUEST_SLIDES_DIR_REREAD
    f = open( outFolder + '/REQUEST_SLIDES_DIR_REREAD', 'w' )
    f.write( "" )
    f.close()  

    return artist, title
