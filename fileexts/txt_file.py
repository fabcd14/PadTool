#!/usr/bin/python3

import string

def parseTxt(file, tmpl):
    artist = ""
    title = ""
    cover = ""

    file = file.decode("utf-8")
    file = file.split('\n')
    tmpl = tmpl.split('\n')

    idxArtistLine = -1
    idxArtistIdx  = -1
    idxTitleLine  = -1
    idxTitleIdx   = -1
    idxCoverLine  = -1
    idxCoverIdx   = -1
    
    lenArtistTag = len("$artist")
    lenTitleTag  = len("$title")
    lenCoverTag  = len("$cover")

    count = 0
    for line in tmpl:
        if ("$artist" in line):
            idxArtistLine = count
            idxArtistIdx  = line.index("$artist")
        if ("$title" in line):
            idxTitleLine = count
            idxTitleIdx  = line.index("title")
        if ("$cover" in line):
            idxCoverLine = count
            idxCoverIdx  = line.index("cover")    
        count = count + 1

    if (idxArtistLine == idxTitleLine):
        file[idxArtistLine] = file[idxArtistLine].strip("\r")
        file[idxArtistLine] = file[idxArtistLine].strip("\n")

        #Case where the artist tag is located on the same line that the title tag
        offset = idxTitleIdx - idxArtistIdx
        separator = ""
        eol = ""
        if (offset > 0):
            #Case where the artist tag is located before the title tag
            separator = tmpl[idxArtistLine][idxArtistIdx+lenArtistTag:idxTitleIdx-1]
            eol = tmpl[idxArtistLine][idxTitleIdx+lenTitleTag-1:]
        elif (offset < 0):
            #Case where the title tag is located before the artist tag
            separator = tmpl[idxTitleLine][idxTitleIdx+lenTitleTag-1:idxArtistIdx]
            eol = tmpl[idxTitleLine][idxArtistIdx+lenArtistTag:]

        lenSeparator = len(separator)
        lenEol = len(eol)
        idxFileSeparator = file[idxArtistLine].index(separator)

        if (offset > 0):
            artist = file[idxArtistLine][idxArtistIdx:idxFileSeparator]
            if (lenEol > 0):
                title  = file[idxTitleLine][idxFileSeparator+lenSeparator:-lenEol]
            else:
                title  = file[idxTitleLine][idxFileSeparator+lenSeparator:]
        elif (offset < 0):
            title = file[idxTitleLine][idxTitleIdx-1:idxFileSeparator]
            if (lenEol > 0):
                artist = file[idxArtistLine][idxFileSeparator+lenSeparator:-lenEol]
            else:
                artist = file[idxArtistLine][idxFileSeparator+lenSeparator:]
    else:
        if(idxArtistLine != -1):
            if(len(tmpl[idxArtistLine]) != lenArtistTag):
                extraBe = tmpl[idxArtistLine].index("$artist")
                extraAf = len(tmpl[idxArtistLine])-(tmpl[idxArtistLine].index("$artist")+lenArtistTag)
                artist = file[idxArtistLine][extraBe:-extraAf]
                print ("[TXT ] Artist value : '" + artist + "'")
            else:
                artist = file[idxArtistLine]
                print ("[TXT ] Artist value : '" + artist + "'")
        if(idxTitleLine != -1):
            if(len(tmpl[idxTitleLine]) != lenTitleTag):
                extraBe = tmpl[idxTitleLine].index("$title")
                extraAf = len(tmpl[idxTitleLine])-(tmpl[idxTitleLine].index("$title")+lenTitleTag)
                title = file[idxTitleLine][extraBe:-extraAf]
                print ("[TXT ] Title value : '" + title + "'")
            else:
                title = file[idxTitleLine]
                print ("[TXT ] Title value : '" + title + "'")
        if(idxCoverLine != -1):
            if(len(tmpl[idxCoverLine]) != lenCoverTag):
                extraBe = tmpl[idxCoverLine].index("$cover")
                extraAf = len(tmpl[idxCoverLine])-(tmpl[idxCoverLine].index("$cover")+lenCoverTag)
                cover = file[idxCoverLine][extraBe:-extraAf]
                print ("[TXT ] Cover value : '" + cover + "'")
            else:
                cover = file[idxCoverLine]
                print ("[TXT ] Cover value : '" + cover + "'")

    if(artist == "" or title == "" or cover == ""):
        print("[TXT ] The following items aren't found :")
        if(artist == ""):
            print("[TXT ] $artist, ")
        if(title == ""):
            print("[TXT ] $title, ")
        if(cover == ""):
            print("[TXT ] $cover")
    return artist, title, cover
