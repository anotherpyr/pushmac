'''
Created on Aug 16, 2015

@author: anotherpyr
'''

import codecs
import os
import platform
import sys
import sqlite3
import time
import pcfilter
import service

class GPodder:
    '''
    A wrapper for gPodder
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        homedir = os.path.expanduser("~")
        self.name = 'gPodder'
        self.service = None
        
        if platform.system() == 'Darwin':
            self.downloads = os.path.join(homedir, "Library/Application Support/gPodder/Downloads")
            self.database = os.path.join(homedir, "Library/Application Support/gPodder/Database")
            self.app = "/Applications/gPodder.app"
            self.resources = os.path.join(self.app, "Contents/Resources")
            self.lib = os.path.join(self.resources, "lib")
            self.data = os.path.join(self.resources, "share")
            self.cmd = os.path.join(self.resources, "bin/gpo")
            self.service = service.Service(self.cmd)

        # Sanity checks
        if not self.service.dirCheck(self.downloads):
            print "gPodder download directory not found: [" + self.downloads + "]"
            sys.exit(-1)

        if not self.service.fileCheck(self.database):
            print "gPodder database not found: [" + self.database + "]" 
            sys.exit(-2)
            
        if self.service.dirCheck(self.lib):
            self.service.setEnv('DYLD_LIBRARY_PATH', self.lib)
            pathroot = os.path.join(self.lib, "python2.7")
            if self.service.dirCheck(pathroot):
                self.service.addToPythonPath(pathroot)
                    
                pathpart = os.path.join(pathroot, "site-packages")
                if self.service.dirCheck(pathpart):
                    self.service.addToPythonPath(pathpart)

        else:
            print "gPodder library not found: [" + self.lib + "]"
            sys.exit(-4)

        if self.service.dirCheck(self.data):
            self.service.setEnv("XDG_DATA_DIRS", self.data)
        else:
            print "xdg data directory not found"

        
    def update(self):
        '''
        Check for updates
        '''
        return self.service.run("update", state="Updating")

        
    def download(self):
        '''
        Download new podcasts
        '''
        return self.service.run("download", state="Downloading")

                
    def getName(self):
        return self.name

        
    def getPodcastDirs(self):
        return os.listdir(self.downloads)


    def getPodcastEpisode(self, podcast):
        episodes = []
        dirname = os.path.join(self.downloads, podcast)
        if os.path.isdir(dirname):
            episodes = os.listdir(dirname)
            
        return episodes

    
    def getAiredDate(self, published):
        airtime = time.gmtime(published)
        aired = str(airtime.tm_year) + u"-"
        if airtime.tm_mon < 10:
            aired = aired + u"0"

        aired = aired + unicode(str(airtime.tm_mon)) + u"-"
        if airtime.tm_mday < 10:
            aired = aired + u"0"
        
        aired = aired + unicode(str(airtime.tm_mday)) + u"T"
        if airtime.tm_hour < 10:
            aired = aired + u"0"

        aired = aired + unicode(str(airtime.tm_hour)) + u":"

        if airtime.tm_min < 10:
            aired = aired + u"0"

        aired = aired + unicode(str(airtime.tm_min)) + u":"
        if airtime.tm_sec < 10:
            aired = aired + u"0"

        aired = aired + unicode(str(airtime.tm_sec)) + u"Z"
        
        return aired

    
    def getEpisodeFilename(self, podcast, episode):
        return os.path.join(os.path.join(self.downloads, podcast), episode)
    
    def getDownload(self, epsisodeFilename):
        return epsisodeFilename[len(self.downloads):]
    
    def getUpload(self, download):
        return self.downloads + download

    def getMetadataFilename(self, videofilename):
        return videofilename + ".txt"

    
    def writeMetadataFile(self, filename, podcastId, podcastTitle, episodeId, episodeTitle, description, published):
        lines = []
        lines.append(u'title : ' + podcastTitle + u' - ' + episodeTitle + u'\n')
        lines.append(u'seriesTitle : ' + podcastTitle + u'\n')
        lines.append(u'episodeTitle : ' + episodeTitle + u'\n')
        lines.append(u'episodeNumber : ' + str(episodeId) + u'\n')
        lines.append(u'isEpisode : true\n')
        lines.append(u'description : ' + description + u'\n')
        lines.append(u'seriesId : PC' + unicode(str(podcastId)) + u'\n')
        lines.append(u"originalAirDate : " + self.getAiredDate(published) + u"\n")
        lines.append(u"tvRating : NR\n")
        lines.append(u'callsign : GPOD\n')
        lines.append(u'vProgramGenre : Podcast\n')
        filename = self.getMetadataFilename(filename)
        print filename
        f = codecs.open(filename, "w", encoding='utf-8')
        for line in lines:
            print line
            f.write(line)
        f.close()

        
    def createMetadata(self, filter=None):
        filesToPush = []
        conn = sqlite3.connect(self.database)
        
        podcasts = self.getPodcastDirs()
        
        if filter == None:
            filter = pcfilter.SimpleDescription()
        
        for podcast in podcasts:
            podcastrs = conn.execute("SELECT id, title FROM podcast WHERE download_folder='" + podcast + "'")
            for id, title in podcastrs:
                episodes = self.getPodcastEpisode(podcast)
                for episode in episodes:
                    filename = self.getEpisodeFilename(podcast, episode)
                    if not self.service.fileCheck(self.getMetadataFilename(filename)):
                        episoders = conn.execute("SELECT id, title, description, published FROM episode WHERE download_filename='" + episode + "'")
                        for eid, etitle, description, published in episoders:
                            filesToPush.append(self.getDownload(filename))
                            desc = filter.filter(description.split("\n"))
                            self.writeMetadataFile(filename, id, title, eid, etitle, desc, published)

        return filesToPush
    
    
    def getService(self):
        return self.service
