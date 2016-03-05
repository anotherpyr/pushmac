
import platform
import os
import json
import sys
import subprocess
from subprocess import PIPE

class Service:
    def __init__(self, command):
        self.pythonCmd = None
        self.command = command
        self.env = None
        self.process = None
        self.state = "Stopped"
        
        if not self.fileCheck(self.command):
            print "Command not found: " + self.command
            sys.exit(-1)
            
        # If Mac OS X, use gpodder supplied python
        if platform.system() == 'Darwin':
            self.app = "/Applications/gPodder.app"
            self.pythonCmd = os.path.join(self.app, "Contents/MacOS/python")
            self.pythonHome = os.path.join(self.app, "Contents/Resources")
            self.env = os.environ.copy()

            if not self.dirCheck(self.pythonHome):
                print "Missing python home directory: [" + self.pythonHome + "]"
            else:
                self.env['PYTHONHOME'] = self.pythonHome
        
        if not self.executableCheck(self.pythonCmd):
            print "python command not found or not executable: [" + self.pythonCmd + "]"
            sys.exit(-2)
        else:
            self.env['PYTHON'] = self.pythonCmd


    def dirCheck(self, path):
        return os.path.exists(path) and os.path.isdir(path)

    
    def fileCheck(self, path):
        return os.path.exists(path) and os.path.isfile(path)


    def executableCheck(self, path):
        return self.fileCheck(path)  and os.access(path, os.X_OK)


    def addToPythonPath(self, value):
        if 'PYTHONPATH' in self.env:
            self.env['PYTHONPATH'] = self.env['PYTHONPATH'] + ":" + value
        else:
            self.env['PYTHONPATH'] = value

            
    def getEnv(self, key):
        value = None
        
        if key in self.env:
            value = self.env[key]
            
        return value

    
    def setEnv(self, key, value):
        self.env[key] = value
        
    
    def getState(self):
        if self.process != None:
            if self.process.poll() is not None:
                self.state = "Stopped"
                
        return self.state
    
    
    def setState(self, state):
        self.state = state
        
        
    def run(self, params=None, state="Running"):
        self.state = state
        args = [self.pythonCmd, self.command]

        if params != None:
            args.append(params)
            
        print "Executing: " + json.dumps(args)
            
        self.process = subprocess.Popen(args, stdout=PIPE, stderr=PIPE, env=self.env)
        return self.process


    def stop(self):
        if self.process != None:
            if self.process.poll == None:
                self.process.terminate()
