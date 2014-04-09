# -*- coding: utf-8 -*-
import tweepy
import codecs
import os
import urllib2
import time
import threading
from BeautifulSoup import BeautifulSoup

URL 		= "http://.../index.php?option=com_content&task=blogcategory&"
FILENAME 	= "tweets.txt"
PAGES 		= ['id=1&Itemid=79','id=24&Itemid=78','id=22&Itemid=82']#'id=26Itemid=83']
SHORTURL	= "http://clck.ru/--?url="

#	ONE MORE SHORT LINKS
#	https://rlu.ru/

CONSUMER_KEY 	= ''
CONSUMER_SECRET = ''
ACCESS_KEY 	= ''
ACCESS_SECRET	= ''


class MyThread(threading.Thread):

 	def __init__(self,site):
 		self.site = site
		threading.Thread.__init__(self)

	def run(self):
		t = Tweetya()
		link = t.parse(self.site)
		urls = t.getlinks()
		for i in link:
			if  not (i in urls):
				t.setlink(i)
				short = t.short(i)
				title = t.gettitle(short)
				print str(title)+' '+str(short)


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
		s = SHORTURL+'http%3A%2F%2F...%2Findex2.php%3Foption%3Dcom_content%26task%3Dview%26id%3D'
		fet = urllib2.urlopen(s+'%s' %url).read()
		return fet

	def gettitle(self,site):
		page = urllib2.urlopen(site).read()
		soup = BeautifulSoup(page)
		soup.prettify()
		text = soup.find(attrs={'class': 'contentheading'})
		if text!=None:
			#title = title.text.encode('utf-8')
			#text = unicode(title, 'utf-8')
			l = len(text)
			if l>118:
			 	text = text[:118-l]
		return text.text.encode('utf-8')


	def parse(self,site):
		data = []
		page = urllib2.urlopen(site).read()
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
	for num in PAGES:
		url = URL+num
		MyThread(url).start()
