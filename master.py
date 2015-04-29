import os
import sys
from processTweets import *
from extract_tweets import *
from computeMetrics import *
from GeneticAlgorithm import *

difficultyLevel={0:"Can I play, Daddy?",1:"Don't hurt me.",2:"Bring 'em on!",3:"I am Death incarnate!"}


def main():
	global difficultyLevel

	username = sys.argv[1]
	pickleFile = username + '.p'
	tweetFile = username + '.out'
	mobaTweetFile = 'mobastatuses.out'

	if not os.path.exists('data/' + tweetFile):
		getTweetsforUser(username,pickleFile)

		processStatuses(pickleFile,tweetFile)

	try:
		with open ("data/" + tweetFile, "r") as myfile:
			userDoc=myfile.read().replace('\n', '')
			print '######### User tweets found #########'
			raw_input()
	except:
		print 'User tweets not found'
		return



	if os.path.exists('data/' + mobaTweetFile):
		with open ("data/mobastatuses.out", "r") as myfile:
			mobaDoc=myfile.read().replace('\n', '')
			print '######### MOBA Tweets found #########'
			raw_input()
	else:
		print 'MOBA Tweets not found'
		return

	similarity = computeSimilarity([mobaDoc,userDoc])

	###WRITE LOGIC TO CONVERT FROM SIMILARITY TO LEVEL!!!
	level = 0
	print "######### Difficulty Level Selected - " + difficultyLevel[level] + " #########"
	raw_input()

	#COMPLETE IMPLEMENTATION OF THIS FUNCTION
	sentiment = computeSentiment(userDoc)
	print "######### User tweet sentiment acertained #########"
	raw_input()

	print "######### Running Generic Algorithm for map generation #########"
	GA(level,sentiment)




if __name__ == '__main__':
	main()