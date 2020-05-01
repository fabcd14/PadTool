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
# -*- coding: utf-8 -*-

from datetime import datetime

def printMsg(topic, msg):
    now = datetime.now()
    dateTime = now.strftime("%Y/%m/%d %H:%M:%S")
    print("[" + dateTime +"]" + " [" + topic + "] " + str(msg))

def formString(s, typeForm = 0):
    if(typeForm == 0):      # As-is
        return s
    elif(typeForm == 1):    # All lower
        return s.lower()
    elif(typeForm == 2):    # All UPPER
        return s.upper()
    elif(typeForm == 3):    # Only The First Letter Of Each Word Upper
        s = s.lower()
        r = ""
        for t in s.split(' '):
            r = r + t.title() + " "
        return r
    else:
        return s