# Author: 			Anton Tkacz 
# Project: 			Crawler link processor
# Last modified:	00:37, 9 April 2014
# Processes all URLs that have been crawled
# This makes sure that if crawler crashes, we have a level of
# redundancy

# DOUBLE CHECK LAST MODIFIED PROPERTY, TOO TIRED

import sys
import datetime
import cPickle as pickle
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
from common import *

# Should exist, otherwise crawl2.py has not been run
try:
	url_file = open("url.pickle", "r")
	# a, b & c not needed in this process, refer to crawl2.py for more info
	a, b, to_mine_all, c = pickle.load(url_file)
	url_file.close()
except:
	print "Run crawl2.py first to generate cache"
	sys.exit(1)

# Check if subjects.pickle exists
try:
	subjects_file = open("subjects.pickle", "r+")
	subject, last_modified = pickle.load(subjects_file)
# Create new instance
except:
	subjects_file = open("subjects.pickle", "w")
	last_modified = parse_date("01-Jan-2000 00:00")
	subject = defaultdict(list)

last_modified_overall = last_modified

for link in to_mine_all.keys():

	# Check if new link to add to cache
	parsed_date = parse_date(to_mine_all[link])
	if parsed_date > last_modified:
		if parsed_date > last_modified_overall:
			last_modified_overall = parsed_date

		try:
			url = link + "presentation.xml"
			lecture_data = parse_url(url)
			soup = BeautifulSoup(lecture_data)

			subject_name = soup.find("name").text
			print subject_name
			date_time = soup.find("start-timestamp").text
			video_url = link + "audio-vga.m4v" 
			audio_url =	link + "audio.mp3" 
			lec = Lecture(date_time, video_url, audio_url)
			subject[subject_name].append(lec)

		except:
			print "No presentation file found, cannot categorize"

pickle.dump([subject, last_modified_overall], subjects_file)
subjects_file.close()