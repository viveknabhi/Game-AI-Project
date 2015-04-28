import cPickle
import string
from nltk.stem.porter import PorterStemmer as ps
from nltk.corpus import stopwords

def tok_tweet(tweet):
    stemmer=ps()
    tweet = tweet.strip()
    words = tweet.split()
    tokenlist = []
    exclude = set(string.punctuation)
    punc = string.punctuation
    punc = punc.replace('#','')
    exclude_punc = set(punc)

    for word in words:
        word = word.strip()
        word = word.lower()

        if word in stopwords.words('english'):
            continue

        #Replace URLs with @http and then with blank
        if word.startswith('www') or word.startswith('http') or word.startswith("@") or word.isdigit() or word == 'rt':
            continue #ignore if word is a url, @mention or contains only numbers or is a stopword
        nword = ''.join(ch for ch in word if ch not in exclude_punc)
        tokenlist.append(stemmer.stem(nword))
    tokens= tokenlist
    return ' '.join(tokens)

def processStatuses(statusFile,textFile):
    corpus = ''
    statuses = cPickle.load(open('data/' + statusFile))
    for status in statuses:
        if status.lang == 'en':
            tweet = tok_tweet(status.text)
            corpus += tweet + ' '

    with open('data/'+textFile,'a') as outFile:
        outFile.write(corpus.encode('utf-8'))

    return corpus


#processStatuses('DendiBoss.p','DendiBoss.out')