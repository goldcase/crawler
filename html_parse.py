import urllib
import re
from BeautifulSoup import BeautifulSoup
from sets import Set

def html_string(url):
	return urllib.urlopen(url).read()

def main():
	# Website with links to all unimelb Echo 360 lectures
	url = "http://aussieservers.net/recordings.htm"
	parsed = html_string(url)
	soup = BeautifulSoup(parsed)

	# Current subjects I am doing
	subject1 = Set(['2014', 'ENGR10004', 'SM1'])
	subject2 = Set(['2014', 'COMP30024', 'SM1'])
	subject3 = Set(['2014', 'INFO30004', 'SM1'])
	subject4 = Set(['2014', 'INFO30005', 'SM1'])
	
	for link in soup.findAll('a', href=True):
		subject = Set(re.split('_|-| ', link.text))

		if subject1.issubset(subject):
			print link['href']

		if subject2.issubset(subject):
			print link['href']

		if subject3.issubset(subject):
			print link['href']

		if subject4.issubset(subject):
			print link['href']

			# Do magic to get the dynamically created website
			# video_url = video_link['href'][:-18]

main()