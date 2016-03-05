
'''
Created on Sep 16, 2015

@author: anotherpyr
'''

from threading import Thread
from Queue import Queue, Empty

class PipeReader:
    def __init__(self, pipe):
        self.queue = Queue()
        self.pipe = pipe
        t = Thread(target=self.enqueue)
        t.daemon = True
        t.start()
    
    def enqueue(self):
        for line in iter(self.pipe.readline, b''):
            self.queue.put(line)
        self.pipe.close()
        
    def readline(self):
        line = None
        try:
            line = self.queue.get_nowait()
        except Empty:
            line = None
        
        return line
