#!/usr/bin/python

'''
Created on Aug 16, 2015

@author: anotherpyr, markp99
'''

import gpodder
import pytivo
import pipereader
from time import sleep

class PushCast:
    '''
    '''
    
    def __init__(self):
        self.verision = '0.1'
        self.gpodder = gpodder.GPodder()
        self.pytivo = pytivo.PyTiVo()

        
    def auto(self):
        self.processWait(self.gpodder.update())
        self.processWait(self.gpodder.download())
        files = self.gpodder.createMetadata()
        print "gPodder done"
        if len(files) > 0:
            print "Starting pyTiVo..."
            process = self.pytivo.runPyTivo()
            sleep(5)
            print "Pushing ..."
            for i in range(len(files)):
                print files[i]
                self.pytivo.push(files[i])    

            self.monitorPyTiVo(process, files)
            
        
    def processWait(self, process):
        output = pipereader.PipeReader(process.stdout)
        error = pipereader.PipeReader(process.stderr)
        while process.poll() is None:
            line = output.readline()
            if line != None:
                print line
            line = error.readline()
            if line != None:
                print "ERROR: " + line

        print "Process completed: " + str(process.poll())


    def monitorPyTiVo(self, process, filenames):
        error = pipereader.PipeReader(process.stderr)
        unmatched = 0
        print "Waiting for " + str(len(filenames)) + " podcasts to complete uploading"
        while process.poll() is None:
            line = error.readline()
            if line != None:
                if 'Done' in line and 'sending' in line:
                    match = None
                    for i in range(len(filenames)):
                        if filenames[i] in line:
                            match = filenames[i]
                            break
                        
                    if match != None:
                        filenames.remove(match)
                        print "Uploading completed for: " + match
                        print "Waiting for " + str(len(filenames)) + " podcasts to complete uploading"
                        # Debugging message
                        for i in range(len(filenames)):
                            print "Pending: " + filenames[i]
                    else:
                        unmatched = unmatched + 1
                        print "No match found for: " + line
                        print "Unable to match " + str(unmatched) + " successful upload messages"
                else:
                    print line
            
            if len(filenames) == 0:
                break
            
        process.terminate()
                    
            
def main():
    pc = PushCast()
    pc.auto()

    
if __name__ == '__main__':
    main()
