#!/usr/bin/env python

import os, sys
import subprocess
import ctypes

from subprocess import Popen, PIPE, STDOUT, call

ctypes.windll.kernel32.SetConsoleTitleA("pushCast Console")

## Variable Defaults ##
myVer = 'v0.1'
myFreq=4
mediaPath="c:\users\mark pelletier\downloads\media"
pyTivoPath="c:\pyTivo\pyTivoService.py"
pythonPath="c:\python27\python.exe"
gPodderPath="c:\program files (x86)\gpodder"

## State Variables ##
state_pyTivo = "Stopped"
state_autoPush="Stopped"
state_gPod = "Waiting"
state_Task = "Stopped"

## Misc Functions ##
def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

def myOS():
    if os.name == "posix":
       myOS = "Linux"
    elif os.name == "nt":
       myOS = "Windows"
    elif os.name == "os2":
      myOS = "Mac"
    else:
    	myOS = "Unknown"
    return myOS

## gPodder ##
def gPodder():
	state_gPod="Running"
	cmd=r"c:\program files (x86)\gpodder"
	os.chdir(cmd);	print
	os.system("gpo update 2>nul"); print
	os.system("gpo download 2>nul")
	state_gPod="Waiting"
	return

## autoPush Toggle ##
def autoPush(action):
	global state_autoPush
	if action=="start":
		cmd= r"c:\pyTivo\service\win32\start-service.bat"
		ap_process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		state_autoPush="Running"
	elif action=="stop":
		cmd= r"c:\pyTivo\service\win32\stop-service.bat"
		ap_process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		state_autoPush="Stopped"

## pyTivo Toggle ##
#def pyTivo(action):
#	global state_pyTivo
#	global py_process
#	if action=="start":
#		cmd = r'c:\Python27\pythonw.exe "{}"'.format(pyTivoPath)
#		py_process = Popen(cmd, stdout=PIPE, stderr=STDOUT)
#		state_pyTivo = "Running"
#	elif action=="stop":
#		py_process.terminate()
#		state_pyTivo = "Stopped"
			
## pyTivo Toggle ##
def pyTivo(action):
	global state_pyTivo
	global py_process
	if action=="start":
		cmd= r"python " + pyTivoPath + " start"
		py_process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)		
		state_pyTivo = "Running"
	elif action=="stop":
		cmd= r"python " + pyTivoPath + " stop"
		py_process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)		
		state_pyTivo = "Stopped"

## Main Menu ##
def main_menu():
	clear_screen()
	print 
	print (35 * '=')
	print " pushCast.py %s" % (myVer)
	print  " OS: %s, PID: %d" % (myOS(), os.getpid())
	print (35* '=')
	print " App Toggles:\n"
	print "   1. pyTivo            [%s]" % (state_pyTivo)
	print "   2. gPodder           [%s]" % (state_gPod)
	print "   3. Auto_Push         [%s]" % (state_autoPush)
	print "   4. Scheduler         [%s]\n" % (state_Task)
	print (35* '=')
	
	print " pushCast:\n"
	print "   A. Run Auto & Exit"
	print "   M. Process Metadata\n"
	print "   G. Launch gPodder GUI"
	print "   V. View autoPush Log\n"
	print "   P. Pause All"
	print "   R. Resume All\n"
	print "   X. Exit pushCast\n"
	print (35 * '=')
	choice=raw_input ("\nSelect: ")
	exec_menu(choice)
	return

## Menu Actions ##
def exec_menu(choice):
	clear_screen()
	
	if choice=="1":
		if state_pyTivo=="Stopped":
			pyTivo("start")
		elif state_pyTivo=="Running":
			pyTivo("stop")

	elif choice=="2":
		gPodder()

	elif choice=="3":
		if state_autoPush=="Stopped":
			autoPush("start")
		elif state_autoPush=="Running":
			autoPush("stop")
		
	elif choice=="6":
		main_menu()
			
	elif choice=="7":
		main_menu()

	elif choice=="8":
		main_menu()

	elif choice=="9":
		main_menu()
		
	elif choice.upper()=="A":
		pyTivo("start")
		autoPush("Start")
		gPodder()
		raise SystemExit

	elif choice.upper()=="M":
		main_menu()

	elif choice.upper()=="P":
		main_menu()

	elif choice.upper()=="R":
		main_menu()
	
	elif choice.upper()=="X":
		raise SystemExit

	else:
		main_menu()

	main_menu()
	
## Main Loop ##	
pyTivo("start")
autoPush("start")
main_menu()
