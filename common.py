# Author: 			Anton Tkacz 
# Project: 			Common tools/classes to crawler-related project
# Last modified:	00:37, 9 April 2014

import datetime
import urllib

# Lecture class wrapper
class Lecture:
	def __init__(self, date_time, video_url, audio_url):
		self.date_time = date_time
		self.video_url = video_url
		self.audio_url = audio_url

# Returns a datetime object from the standard date string used on the 
# echo server
def parse_date(date_string):
	return datetime.datetime.strptime(date_string, "%d-%b-%Y %H:%M")

# Returns a parsed URL as plain text
def parse_url(url):
	return urllib.urlopen(url).read()