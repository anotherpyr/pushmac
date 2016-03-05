
import os;
import ConfigParser

class PushConfig:
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.filename = os.path.join(self.home, 'pushcast.conf')
        self.config = ConfigParser.RawConfigParser()

        if os.path.isfile(self.filename):
            self.loadParameters()
        else:
            self.getParamters()


    def loadParameters(self):
        config.read(self.filename)

    def getParameters(self):
        # Section 1: Pushcast
        # Section 2: gPodder
        # Section 3: pyTivo
        # Prompt for parameter values per each section
        with open(self.filename, 'wb') as configfile:
            config.write(configfile)
