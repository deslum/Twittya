# -*- coding: utf-8 -*-
import tweepy
import codecs
import urllib2
import threading
import MySQLdb
import string
from threading import BoundedSemaphore
from BeautifulSoup import BeautifulSoup


URL 		= "http://www.kolomna-kgpi.ru/index.php?option=com_content&task=blogcategory&"
FILENAME 	= "tweets.txt"
PAGES 		= ['id=1&Itemid=79','id=24&Itemid=78','id=22&Itemid=82','id=26&Itemid=83']
MAXCONN		= 1

CONSUMER_KEY 	= ''
CONSUMER_SECRET = ''
ACCESS_KEY 	= ''
ACCESS_SECRET	= ''


class MyThread(threading.Thread):

 	def __init__(self,site):
 		self.site = site
		threading.Thread.__init__(self)
		self.semaphore = BoundedSemaphore(value=MAXCONN)
		self.t = Tweetya()

	def run(self):
		link = self.t.parse(self.site)
		self.semaphore.acquire() 
		urls = self.t.getlinks()
		for i in link:
			if  not (i in urls):
				self.t.setlink(i)
				short = self.t.short(i)
				title = self.t.gettitle(short)
				print str(title)+' '+str(short)
		self.semaphore.release()


class Tweetya(object):

	def auth(self):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		api.update_status('Проба пера')

	
	def getlinks(self):
		db = MySQLdb.connect(host="localhost", user="root", passwd="пароль", db="contacts", charset='utf8')
		cursor = db.cursor()
		sql = """SELECT mail, name FROM eadres WHERE mail LIKE '%yandex.ru' LIMIT 10"""
		cursor.execute(sql)
		data =  cursor.fetchall()
		db.close()
		return data 
		#links=[]
		#try:
		#	handle = open(FILENAME,"r")
		#	for line in handle.readlines():
		#		links.append(line)
		#except:
		#	print "Error read file"
		#handle.close
		#return links

	def setlink(self,link):
		db = MySQLdb.connect(host="localhost", user="root", passwd="пароль", db="contacts", charset='utf8')
		cursor = db.cursor()
		sql = """INSERT mail, name FROM eadres WHERE mail LIKE '%yandex.ru' LIMIT 10"""
		cursor.execute(sql)
		data =  cursor.fetchall()
		db.close()
		#try:
		#	handle = open(FILENAME,'a')
		#	handle.write(link);
		#	handle.close
		#except:
		#	print "Error read file"

	def short(self,url):
		s = 'http://clck.ru/--?url=http%3A%2F%2Fwww.kolomna-kgpi.ru%2Findex2.php%3Foption%3Dcom_content%26task%3Dview%26id%3D'
		fet = urllib2.urlopen(s+'%s' %url).read()
		return fet

	def gettitle(self,site):
		page = urllib2.urlopen(site).read()
		soup = BeautifulSoup(page)
		soup.prettify()
		text = soup.find(attrs={'class': 'contentheading'})
		l = 0
		l = len(text)
		if l>118:
			text = text[:118-l]
		text = text.text.encode('utf-8')
		return text

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
