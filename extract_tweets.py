import tweepy
import cPickle
import time
from configFile import *

statuses = []
tweets = []
count = 0

def generateTweepyObject():
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(key, secret)
	api = tweepy.API(auth)
	return api


def getTweetsforTag(tag,fileName):
	API = generateTweepyObject()
	pageIterator = tweepy.Cursor(api.search, q=tag).pages()
	pickleFile = open("data/" + fileName,'wb')

	while True:
		try:
			page = pageIterator.next()
			for status in page:
				if status.lang == 'en':
					statuses.append(status)
					tweets.append(status.text)
		except:
			cPickle.dump(statuses, pickleFile)
			print "started sleep at: ", time.ctime(), count
			tweets = []
			statuses = []
			time.sleep(100)


def getTweetsforTag(tag,fileName):
	API = generateTweepyObject()
	pageIterator = tweepy.Cursor(api.search, q=tag).pages()
	pickleFile = open("data/" + fileName,'wb')

	while True:
		try:
			page = pageIterator.next()
			for status in page:
				if status.lang == 'en':
					statuses.append(status)
					tweets.append(status.text)
					print status.text
		except:
			cPickle.dump(statuses, pickleFile)
			print "started sleep at: ", time.ctime(), count
			tweets = []
			statuses = []
			time.sleep(100)


def getTweetsforUser(username,fileName):
	API = generateTweepyObject()
	statusIterator = tweepy.Cursor(api.user_timeline, id=username).items()
	pickleFile = open("data/" + fileName,'wb')

	while True:
		try:
			status = statusIterator.next()
			if status.lang == 'en':
				statuses.append(status)
				tweets.append(status.text)
				print status.text
		except:
			cPickle.dump(statuses, pickleFile)
			print "started sleep at: ", time.ctime(), count
			tweets = []
			statuses = []
			time.sleep(100)



getTweetsforUser('viveknabhi','viveknabhi.p')