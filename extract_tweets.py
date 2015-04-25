import tweepy
import cPickle
import time

consumer_token = "BqQJc1GpaFSAEvih0cATu87Fb"
consumer_secret = "ZpHWc4ejiZaEbLtgmcWbOapFLg3hCPvvOWWcXUNcJvTtBgU4eS"
key = "450460896-rCRHB0dhED0aK3i60cp66hktZ7oW2rmt2vB1JoJR"
secret = "HI8YvDJT1oxUPaq442xc8kSUw5rDo2i0T22ja0h4b3Gi7"

statuses = []

def main():
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	auth.set_access_token(key, secret)
	api = tweepy.API(auth)
	return api

if __name__ == "__main__":
	api = main()

pageIterator = tweepy.Cursor(api.search, q='#dota2').pages()

while True:
	tweets = []
	try:
		page = pageIterator.next()
		for status in page:
			statuses.append(status)
			tweets.append(status.text)
	except:
		with open('dotaTweets.txt','a') as filename:
			for tweet in tweets:
				filename.write(tweet.encode('utf-8'))
				filename.write('\n')
		print "started sleep at: ", time.ctime()
		time.sleep(300)