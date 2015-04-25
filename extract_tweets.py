import tweepy
import cPickle
import time
from configFile import *

statuses = []
tweets = []
count = 0

pickleFile = open("data/statuses.p",'wb')

def main():
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(key, secret)
	api = tweepy.API(auth)
	return api

if __name__ == "__main__":
	api = main()

pageIterator = tweepy.Cursor(api.search, q='#dota2').pages()

while True:
	try:
		page = pageIterator.next()
		for status in page:
			if status.lang == 'en':
				statuses.append(status)
				tweets.append(status.text)
	except:
		cPickle.dump(statuses, pickleFile)
		with open('dotaTweets.txt','a') as filename:
			for tweet in tweets:
				filename.write(tweet.encode('utf-8'))
				filename.write('\n')
		count += len(tweets)
		print "started sleep at: ", time.ctime(), count
		tweets = []
		statuses = []
		time.sleep(100)
