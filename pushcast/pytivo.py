
import os
import service
import urllib
import urllib2
                    
class PyTiVo:
    def __init__(self):
        self.location = os.path.join(os.path.expanduser("~"),  'Downloads/pytivo-master')
        self.pytivo = os.path.join(self.location, 'pyTivo.py')
        self.config = os.path.join(self.location, 'pyTivo.conf')
        self.host = 'localhost'
        self.port = 9032
        self.header = 'http://' + self.host + ':' + str(self.port) + "/TiVoConnect?"
        self.params = {'Command': 'Push', 'Container': 'MyMovies', 'tsn': 'Media Room'}
        self.service = service.Service(self.pytivo)

        
    def push(self, file):
        self.params['File'] = file
        self.geturl = self.header + urllib.urlencode(self.params)
        print "URL: " + self.geturl
        response = urllib2.urlopen(self.geturl)
        print response.read()
        
    
    def runPyTivo(self):
        return self.service.run()

    
    def getService(self):
        return self.service
    
    
    def getName(self):
        return 'pyTiVo'
