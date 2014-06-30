# Author: 			Anton Tkacz 
# Project: 			Echo 360 @ unimelb crawler
# Last modified:	00:37, 9 April 2014
# New functionality that stores a cache of previously crawled web pages
# to speed up crawling, current cache size as of 00:01, 9 April 2014
# is 14.1 megabytes, and yeah, it took a while to crawl.
# It will now only scrape new links which currently are not in cache

import datetime
import cPickle as pickle
from BeautifulSoup import BeautifulSoup
from common import *

# Given a url on echo server, a length of link being searched,
# a datetime object of the latest modified link overall and a datetime object
# of the latest modified link prior to the execution of this instance of
# the crawler, it returns a dictionary with key: link and value: date modified
def scrape_url(url, link_length, last_modified_overall, last_modified):
	to_mine = {}

	html = parse_url(url)
	soup = BeautifulSoup(html)

	for label in soup.findAll('table')[0].findAll('td', attrs={'valign': 'top'}):
		link = label.findNextSiblings()[0].text

		# link_length checks the length of the hyperlink to see if it 
		# agrees with the link we are searching for
		# Top level ####/ - 5
		# Middle leve #/ - 2
		# Bottom level #...#/ - 37
		if len(link) == link_length:
			mod_date_string = label.findNextSiblings()[1].text
			mod_date = parse_date(mod_date_string)

			if mod_date > last_modified:
				if mod_date > last_modified_overall:
					last_modified_overall = mod_date

				this_url = url + link
				to_mine[this_url] = mod_date_string

	return to_mine, last_modified_overall

# Check if a cache exists
try:
	url_pickle = open("url.pickle", "r+")
	to_mine_orig, to_mine_middle_orig, \
	to_mine_all_orig, last_modified = pickle.load(url_pickle)
	original_exists = True
	
	print "Cache found"
	print "Latest scrape found in cache:", last_modified
	print "Updating..."

# Building cache, this will take a while...
# Watch a TV show, maybe grab some chips :P
except:
	url_pickle = open("url.pickle", "w")
	# Random date definitely before echo 360 logs on file
	last_modified = parse_date("01-Jan-2000 00:00")
	original_exists = False
	
	print "Cache not found"
	print "Building cache, it will take A LOT OF TIME"

# Last folder modification date in this round of crawling
last_modified_overall = last_modified

top_url = "http://download.lecture.unimelb.edu.au/echo360/"

# Searches for folder modifications compared to latest crawl, otherwise
# scrapes all folders. This occurs in all of the three processes below
to_mine = {}
to_mine, last_modified_overall = scrape_url(top_url, 5, 
								 last_modified_overall, last_modified)
print to_mine

to_mine_middle = {}
for top_link in to_mine.keys():
	middle_section, last_modified_overall = \
	scrape_url(top_link, 2, last_modified_overall, last_modified)
	to_mine_middle.update(middle_section)
print to_mine_middle

to_mine_all = {}
for middle_link in to_mine_middle.keys():
	bottom_section, last_modified_overall = \
	scrape_url(middle_link, 37, last_modified_overall, last_modified)
	to_mine_all.update(bottom_section)
print to_mine_all

# Update all original dictionaries from cache with newly scraped data, 
# and overwrites it in preparation for pickling
if original_exists == True:
	to_mine_orig.update(to_mine)
	to_mine = to_mine_orig
	to_mine_middle_orig.update(to_mine_middle)
	to_mine_middle = to_mine_middle_orig
	to_mine_all_orig.update(to_mine_all)
	to_mine_all = to_mine_all_orig

print "Latest scrape: ", last_modified_overall

pickle.dump([to_mine, to_mine_middle, to_mine_all, \
	last_modified_overall], url_pickle)
url_pickle.close()