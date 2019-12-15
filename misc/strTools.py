#!/usr/bin/python3
# -*- coding: utf-8 -*-

def parseCharsForImg(content):
    content = content.replace("’", "'")

    content = content.replace("à", "a")
    content = content.replace("á", "a")
    content = content.replace("â", "a")
    content = content.replace("â", "a")
    content = content.replace("ä", "a")
    content = content.replace("ã", "a")

    content = content.replace("À", "A")
    content = content.replace("Á", "A")
    content = content.replace("Â", "A")
    content = content.replace("Ä", "A")
    content = content.replace("Ã", "A")

    content = content.replace("ç", "c")

    content = content.replace("Ç", "C")

    content = content.replace("é", "e")
    content = content.replace("è", "e")
    content = content.replace("ê", "e")
    content = content.replace("ë", "e")

    content = content.replace("É", "E")
    content = content.replace("È", "E")
    content = content.replace("Ê", "E")
    content = content.replace("Ë", "E")

    content = content.replace("î", "i")
    content = content.replace("ï", "i")

    content = content.replace("Î", "I")
    content = content.replace("Ï", "I")

    content = content.replace("ô", "o")
    content = content.replace("ö", "o")

    content = content.replace("Ô", "O")
    content = content.replace("Ö", "O")

    content = content.replace("ù", "u")
    content = content.replace("û", "u")
    content = content.replace("ü", "u")

    content = content.replace("Ú", "U")
    content = content.replace("Û", "U")
    content = content.replace("Ü", "U")
    
    content = content.replace("ÿ", "y")

    content = content.replace("Ÿ", "Y")

    content = content.replace("œ", "oe")
    content = content.replace("Œ", "OE")

    return content