#coding=utf-8
#! /usr/bin/python


import os
import time
import glob
import re
from sys import argv
import sys
import log

reload(sys)
sys.setdefaultencoding('utf-8')

NOTE = "//"
# model
MODEL_START = "@interface"
MODEL_END = "@end"
PROPERTY = "@property"
# enum
ENUM_START = "typedef NS_ENUM"
ENUM_END = "};"

class ClassType:
	NONE = 0
	MODEL = 1
	ENUM = 2

def traslate_to_swift(fp):
	f = open(fp)
	line = f.readline()

	processing = False
	classname = ""
	classtype = ClassType.NONE

	while line:
		line = line.strip('\n').strip()
		if len(line) == 0:
			line = f.readline()
			continue
		# print("line: %s" % line)
		if processing == False:
			new_classname = process_model_start(line)
			if new_classname is None:
				new_classname = process_enum_start(line)
				if new_classname is not None: classtype = ClassType.ENUM
			else:
				classtype = ClassType.MODEL
			if new_classname is not None:
				classname = new_classname
				processing = True
		else:
			if classtype == ClassType.MODEL:
				if process_model_end(line):
					processing = False
					classname = ""
					classtype = ClassType.NONE
				else:
					if not process_note(line): process_property(line)
			elif classtype == ClassType.ENUM:
				if process_enum_end(line):
					processing = False
					classname = ""
					classtype = ClassType.NONE
				else:
					if not process_note(line): process_enum_item(line, classname)
				
		line = f.readline()

def process_model_start(line):
	if line.startswith(MODEL_START) == False: return None
	model = line.split(':')[0][len(MODEL_START):].strip()
	log.printstr("struct %s: Codable {" % (model), "yellow")
	return model

# model
def process_model_end(line):
	result = line.startswith(MODEL_END)
	if result: log.printstr("}\n", "yellow")
	return result

def process_property(line):
	is_property = line.startswith(PROPERTY)
	if not is_property: return False
	pandnote = line.split(';')
	if len(pandnote) > 1 and len(pandnote[1]) > 0: log.printstr("    " + pandnote[1], "yellow")
	propertyline = pandnote[0]
	propertyline = propertyline.split(")")[1].strip()
	propertyinfo = propertyline.split('*')
	ptype = propertyinfo[0].strip()
	pname = propertyinfo[len(propertyinfo) - 1].strip()
	log.printstr("    var %s: %s?" % (pname, type2swift(ptype)), "yellow")
	return is_property

def type2swift(ptype):
	if ptype == "NSString" or ptype == "NSNumber": return "String"
	if ptype == "int" or ptype == "NSInteger": return "Int"
	if ptype.startswith("NSArray"):
		newtype = ptype.split('<')[1].split('>')[0]
		newtype = newtype.replace("*", "").strip()
		return ("Array<%s>" % (newtype))
	if ptype.startswith("NS"): return ptype[2:]
	return ptype

def process_note(line):
	isnote = line.startswith(NOTE)
	if isnote: log.printstr("    " + line.strip(), "yellow")
	return isnote

# enum
def process_enum_start(line):
	if not line.startswith(ENUM_START): return None
	name = line.split(',')[1].strip('){ ')
	log.printstr("enum " + name + " : Int {", "yellow")
	return name

def process_enum_end(line):
	if not line.startswith(ENUM_END): return False
	log.printstr("}\n", "yellow")
	return True

def process_enum_item(line, name):
	if not line.startswith(name): 
		if line.startswith(name[:2]): log.printstr(line, 'b_red')
		return False
	enuminfos = line.split('//')
	enumstr = enuminfos[0]
	if len(enuminfos) > 1: 
		enumnote = enuminfos[1].strip()
		if len(enumnote) > 0: log.printstr("    /// " + enumnote, "yellow")
	enumstr = enumstr[len(name):].strip(', ')
	if enumstr[0].isupper(): enumstr = enumstr[0].lower() + enumstr[1:] 
	log.printstr("    case " + enumstr, "yellow")
	return True

if __name__ == '__main__':
    if len(argv) < 2:
    	log.printstr("Parameters error. Usage: python %s file" % (__file__), "b_red")
    	exit(0)
    filepath = argv[1]
    traslate_to_swift(filepath)
    