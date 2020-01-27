#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime

def printMsg(topic, msg):
    now = datetime.now()
    dateTime = now.strftime("%Y/%m/%d %H:%M:%S")
    print("[" + dateTime +"]" + " [" + topic + "] " + str(msg))