# -*- coding: utf-8 -*-
import tweepy
import codecs
import os
import urllib2
import time
import webbrowser
from BeautifulSoup import BeautifulSoup

URL = "http://www.kolomna-kgpi.ru/index.php?option=com_content&task=blogcategory&id=1&Itemid=79"
FILENAME = "tweets.txt"

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

class Tweetya(object):

	def __init__(self):
		return		

	def auth(self):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		api.update_status('Проба пера')

	
	def getlinks(self):
		links=[]
		try:
			handle = open(FILENAME,"r")
			for line in handle.readlines():
				links.append(line)
		except:
			print "Error read file"
		handle.close
		return links

	def setlink(self,link):
		try:
			handle = open(FILENAME,'a')
			handle.write(link);
			handle.close
		except:
			print "Error read file"

	def short(self,url):
		s = 'http://clck.ru/--?url=http%3A%2F%2Fwww.kolomna-kgpi.ru%2Findex2.php%3Foption%3Dcom_content%26task%3Dview%26id%3D'
		fet = urllib2.urlopen(s+'%s' %url).read()
		return fet

	def gettitle(self,site):
		page = urllib2.urlopen(site).read()
		soup = BeautifulSoup(page)
		soup.prettify()
		title = soup.find(attrs={'class': 'contentheading'})
		if title!=None:
			title = title.text.encode('utf-8')
			if len(title)>118:
			 	title = title[:118-len(title)]
		return title


	def parse(self):
		data = []
		page = urllib2.urlopen(URL).read()
		soup = BeautifulSoup(page)
		soup.prettify()
		for anchor in soup.findAll(attrs={'class': 'contentpaneopen'}): 
			link = anchor.find(attrs={'class': 'buttonheading'})
			if link!=None:
				link = link.find(name = 'a').get('href')
				link = link[70:-21]
				data.append(link+'\n')
		return data



if __name__ == '__main__':
	t = Tweetya()
	link = t.parse()
	urls = t.getlinks()
	for i in link:
		if  not (i in urls):
			t.setlink(i)
			short = t.short(i)
			title = t.gettitle(short)
			print title+' '+short
	t.auth() 
