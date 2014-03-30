# -*- coding: utf-8 -*-
import tweepy
import codecs
import os
import urllib2
import time
from BeautifulSoup import BeautifulSoup

URL = "http://www.kolomna-kgpi.ru/index.php?option=com_content&task=blogcategory&id=1&Itemid=79"

class Tweetya(object):

	def __init__(self):
		CONSUMER_KEY = ""
		CONSUMER_SECRET = ""
		ACCESS_KEY = ""
		ACCESS_SECRET = ""
		URL = ""
		FILENAME = "tweets.txt"

	def auth():
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		return api
	
	def getlinks(self):
		try:
			handle = open(FILENAME,"r")
			for line in handle.readlines():
				links.append(line)
		except:
			print "Error read file"
		fi.close
		return links

	def setlink(self,link):
		handle = open(FILENAME,'a')
		handle.write(link);
		handle.close

	def short(self,url):
		s = 'http://clck.ru/--?url=http%3A%2F%2Fwww.kolomna-kgpi.ru%2Findex2.php%3Foption%3Dcom_content%26task%3Dview%26id%3D'
		fet = urllib2.urlopen(s+'%s' %url).read()
		return fet

	def parse(self):
		page = urllib2.urlopen(URL).read()
		soup = BeautifulSoup(page)
		soup.prettify()
		for anchor in soup.findAll(attrs={'class': 'contentpaneopen'}): 
			title = anchor.find(attrs={'class': 'contentheading'})
			link = anchor.find(attrs={'class': 'buttonheading'})
			if title!=None:
			 	title = title.text.encode('utf-8')
			 	if len(title)>118:
			 		title = title[:118-len(title)]
			if link!=None:
				link = link.find(name = 'a').get('href')
				link = self.short(link[70:-21])
				tweet = str(title)+' '+str(link)
				print tweet



if __name__ == '__main__':
	t = Tweetya()
	t.parse()
