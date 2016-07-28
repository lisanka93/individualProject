import nltk
from nltk.stem import SnowballStemmer



with open('engl_american_10.txt', 'r') as myfile:
	data= myfile.read().replace('\n', ' ')
	data = data.split()

wordlist = [w for w in data]
wordset = set(wordlist)
wordlist = list(wordset)


snowball = SnowballStemmer("english")

stemmed_words = [snowball.stem(w) for w in wordlist]
stemmed_words_google = [w.encode('utf-8') for w in stemmed_words]

print stemmed_words_google
print len(stemmed_words_google)