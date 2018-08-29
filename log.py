#coding:utf-8
#! /usr/bin/python

# 有颜色的打印工具

import os
import sys
from sys import argv
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

TEXT_STYLE = {
    # bold style
    "b_":   "1", 
    # underline style
    "l_":    "2",
    # oblique
    "o_":   "3",
}

FOREGROUND_COLORS  = {
    "black":    "30",
    "red":      "31",
    "green":    "32",
    "yellow":   "33",
    "blue":     "34",
    "purple":   "35",
    "cyan":     "36",
    "white":    "37",
}

BACKGROUND_COLORS  = {
    "black":    "40",
    "red":      "41",
    "green":    "42",
    "yellow":   "43",
    "blue":     "44",
    "purple":   "45",
    "cyan":     "46",
    "white":    "47",
}

def color_from_string(color):
    if not color or len(color) == 0:
        return None
    style = TEXT_STYLE.get(color[0:2])
    fore_color = None
    back_color = None
    color_attrs = color.split('_')
    if style is not None:
        color_attrs = color_attrs[1:len(color_attrs)]
    if len(color_attrs) == 1:
        fore_color = FOREGROUND_COLORS.get(color_attrs[0])
    elif len(color_attrs) >= 2:
        fore_color = FOREGROUND_COLORS.get(color_attrs[0])
        back_color = BACKGROUND_COLORS.get(color_attrs[1])
    result = ""
    if style is not None:
        result = style
    if len(result) > 0:
        result = result + ";" + fore_color
    else:
        result = fore_color
    if back_color is not None:
        result = result + ";" + back_color
    result = result + "m"
    return result


def printstr(string, color="b_white"):
    if not string or len(string) == 0: return
    print ("\033[" + color_from_string(color) + string + "\033[0m")

def printerr(string, index):
    error = "Error! Line:%d: %s" % (index, string)
    printstr(error)

def printarr(array, title="Array", color="b_white"):
    printstr("print array(%s, count:%d) start:" % (title, len(array)))
    string = ""
    for value in array:
        if len(string) > 0:
            string = string + "\n"
        string = string + ("%s" % (value))
    printstr(string, color)
    printstr("print array(%s, count:%d) end." % (title, len(array)))

def printpg(progress, total):
    maxCount = 40
    ratio = progress * 1.0 / total 
    progress_count = int(round(ratio * maxCount))
    result = "progress: " + "✓" * progress_count + "✘" * (maxCount - progress_count) + ("    %05.2f%%" % (ratio * 100))
    printstr(result, "o_yellow")

