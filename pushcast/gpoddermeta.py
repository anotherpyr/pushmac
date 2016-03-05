#!/usr/bin/python

from os import listdir
from os.path import isdir, isfile, join
from time import gmtime
import codecs
import sqlite3

homedir = "/Users/werye"
downloads = homedir + "/Library/Application Support/gPodder/Downloads"
database = homedir + "/Library/Application Support/gPodder/Database"

c = sqlite3.connect(database)
podcasts = listdir(downloads)

for podcast in podcasts:
	dirname = join(downloads, podcast)
	if isdir(dirname):	
		res = c.execute("SELECT id, title FROM podcast WHERE download_folder='" + podcast + "'")
		for id, title in res:
			episodes = listdir(dirname)
			for episode in episodes:
				eres = c.execute("SELECT id, title, description, published FROM episode WHERE download_filename='" + episode + "'")
				for eid, etitle, description, published in eres:
					filename = join(dirname, episode)
					airtime = gmtime(published)
					lines = []
					lines.append(u'title : ' + title + u' - ' + etitle + u'\n')
					lines.append(u'seriesTitle : ' + title + u'\n')
					lines.append(u'episodeTitle : ' + etitle + u'\n')
					lines.append(u'episodeNumber : ' + str(eid) + u'\n')
					lines.append(u'isEpisode : true\n')
					dlines = description.split("\n")
					description = ""
					for k in range(0, len(dlines)):
						description = description + u" " + dlines[k]
					lines.append(u'description : ' + description + u'\n')
					lines.append(u'seriesId : PC' + unicode(str(id)) + u'\n')
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

					lines.append(u"originalAirDate : " + aired + u"\n")
					filename = filename + ".txt"
					f = codecs.open(filename, "w", encoding='utf-8')
					for line in lines:
						f.write(line)
					f.close()

