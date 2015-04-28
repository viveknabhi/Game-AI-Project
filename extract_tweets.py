import tweepy
import cPickle
import time
from configFile import *
from processTweets import *


def generateTweepyObject():
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(key, secret)
	api = tweepy.API(auth)
	return api


def getTweetsforTag(tag,fileName):
	API = generateTweepyObject()
	pageIterator = tweepy.Cursor(api.search, q=tag).pages()
	pickleFile = open("data/" + fileName,'wb')

	statuses = []
	tweets = []
	count = 0

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


def getTweetsforUser(username,fileName):
	api = generateTweepyObject()
	statusIterator = tweepy.Cursor(api.user_timeline, id=username).items()
	pickleFile = open("data/" + fileName,'wb')

	statuses = []
	tweets = []
	count = 0

	while True:
		try:
			status = statusIterator.next()
			if status.lang == 'en':
				statuses.append(status)
				tweets.append(status.text)
				print status.text
				count += 1
		except:
			cPickle.dump(statuses, pickleFile)
			if count < 100:
				return

			if count > 2000:
				return
			print "started sleep at: ", time.ctime(), count
			tweets = []
			statuses = []
			time.sleep(100)



username = 'SUNSfanTV'
getTweetsforUser(username,username+'.p')
processStatuses(username+'.p',username+'.out')