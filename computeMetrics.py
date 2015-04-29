from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from nltk.stem.porter import PorterStemmer as ps

def computeSimilarity(documents):
	tfidf = TfidfVectorizer().fit_transform(documents)
	# no need to normalize, since Vectorizer will return normalized tf-idf
	pairwise_similarity = tfidf * tfidf.T
	#print pairwise_similarity.A[0][1]
	return pairwise_similarity.A[0][1]



def computeSentiment(document):
	senti=pickle.load(open('sentiWordNet.p'))
	updatedSenti = {}
	stemmer = ps()
	for word in senti:
		updatedSenti[stemmer.stem(word[:-2])]=senti[word]

	pos = 0
	neg = 0
	neu = 0
	count = 0
	for word in document.split():
		if word in updatedSenti:
			pos += updatedSenti[word]['posScore']
			#neg += updatedSenti[word]['negScore']
			#neu += updatedSenti[word]['neuScore']
			count += 1
		else:
			pass
			#print word
	#print (float)(pos)/count
	#print (float)(neg)/count
	#print (float)(neu)/count
	return (float)(pos)/count









# mobaData = ''
# user1Data = ''
# user2Data = ''
# user3Data = ''
# user4Data = ''

# with open ("data/mobastatuses.out", "r") as myfile:
#     mobaData=myfile.read().replace('\n', '')

# with open ("data/vinaykola.out", "r") as myfile:
# 	user1Data=myfile.read().replace('\n', '')

# with open ("data/PurgeGamers.out", "r") as myfile:
#     user2Data=myfile.read().replace('\n', '')

# with open ("data/tuxerman.out", "r") as myfile:
#     user3Data=myfile.read().replace('\n', '')


# with open ("data/SUNSfanTV.out", "r") as myfile:
#     user4Data=myfile.read().replace('\n', '')


# documents = [mobaData,user1Data,user2Data,user3Data,user4Data]
# computeSimilarity(documents)

