#FUNCTIONS FOR INDIVIDUAL ARGUMENTS

import nltk,re
from nltk.tokenize import word_tokenize, sent_tokenize
from wordlists import*  #for keywords
from badwords import*
from abbreviations import*
from collections import Counter
from nltk.tag import pos_tag
from enchant.checker import SpellChecker
from not_ne_list import *
from nltk.collocations import *
from nltk.probability import FreqDist

######################################## preprocessing indifivual arguments #####################################################################


def preprocess_argumentI(debate):
	"""sets everything to lower and also removes hyperlinks from argument - returns STRING"""
	
	debate = debate.lower() 

	links = re.findall(r'(w?w?w?.?https?://[^\s]+)', debate)

	x = len(links)

	if x != 0:
		for link in links:
			debate = debate.replace(link, '')
	
	return debate                  


def preprocess_argumentII(debate):
	#removes punctuation APART FROM APOSTROPHE and sets to lower
	
	debate = re.sub("[^\w\d'\s]+", "", debate)  
	#debate = debate.lower()
	return debate


def preprocess_argumentIII(debate):
	#also removes apostrophe and splits argument - returns list

	debate = re.sub("'", "", debate)   
	debate = debate.split()
	return debate


def preprocess_argumentIV(debate):
	#all of the above plus no stopwords

	debate = debate.lower() 
	debate = re.sub("[^\w\d'\s]+", "", debate)  
	debate = debate.split()
	with open('SmartStoplist.txt', 'r') as myfile:
		data=myfile.read().replace('\n', ' ')
	
	data=data.split()

	meaningful_words = [w for w in debate if not w in data and w.isalpha()]
	
	return meaningful_words  

#counts linkingwords in a post - should normalise it
def linkingwordcount(argument):
	
	linking_words = explanation + additional + contrast + proviso + example + importance + other + result + quotes + conclusion
	
	d = dict((i, argument.count(i)) for i in linking_words)
	keyWordCounter = sum(d.values())

	return keyWordCounter

#readability
def ColemanLiauIndex(argument):

	tokenized = word_tokenize(argument)
	
	argument_no_punct = [w for w in tokenized if w.isalpha()]
	stringI = ' '.join(w for w in argument_no_punct)

	letters = len(stringI)
	sentences = len(nltk.sent_tokenize(argument))
	words =  len(argument_no_punct)
	
	outcome = (5.879851 * letters / words - 29.587280 * sentences / words - 15.800804)

	return outcome


def badwordcount(argument):

	numWords = len(argument)

	d = dict((i, argument.count(i)) for i in bad_words)
	badwordCounter = sum(d.values())

	return badwordCounter


def spellCheck(argument): 

	words =  len(argument)
	abbr = abb1 + abb2 + abb3
	#print words

	errors = 0                             
	chkr = SpellChecker("en_GB", argument)

	for word in argument:
		if chkr.check(word) == False:
			errors+=1
			if (chkr.check(word.upper()) == True) or (chkr.check(word.capitalize()) == True) or (chkr.check(word + ".") == True or (word in abbr)):
				errors-=1                                   

	outcome = (float(errors) / words)

	return outcome


def punctCount(argument):

	counts = Counter(argument)
	punctuation = '?!.'                     
	punct_count ={k: v for k, v in counts.iteritems() if k in punctuation}

	sumP = sum(punct_count.values())
	sentences = len(nltk.sent_tokenize(argument))

	outcome = (float(sumP) / sentences)
	return outcome


def percentCount(argument):
	perCount = argument.count('%')
	return perCount



def countDigits(argument):
	digits = sum(c.isdigit() for c in argument)
	return digits




def containsHyperlink(argument):         
	links = re.findall(r'(w?w?w?.?https?://[^\s]+)', argument)
	for link in links:
		argument = argument.replace(link, '')

	return len(links)



def capsCount(argument):
	capwords = 0
		
	for word in argument:
		if word == word.upper() and len(word) > 1:
			capwords +=1

	numWords = len(argument)
	percentCapwords = (float(capwords) / numWords)

	return percentCapwords


def preprocess_for_nee_and_print_ind(argument):                      
	sentences = nltk.sent_tokenize(argument)
	tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

	entity_names = []

	for tree in chunked_sentences:
		#tree.draw()
		entity_names.extend(extract_entity_names_ind(tree))

	#print entity_names
	named_entities = [w for w in entity_names if w not in not_NE]
	named_entities = set(named_entities)
	named_entities = list(named_entities)
	return named_entities



def extract_entity_names_ind(tree):
    entity_names = []

    if hasattr(tree, 'label') and tree.label:
        if tree.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in tree]))
        else:
            for child in tree:
                entity_names.extend(extract_entity_names_ind(child))

    return entity_names



def nouns_in_argument(argument):
	tagged = pos_tag(argument)
	
	propernouns = [word for word,pos in tagged if pos == 'NNP'] 
	nnouns = [word for word,pos in tagged if pos == 'NN']
	nounss = [word for word,pos in tagged if pos == 'NNS']
	
	nouns = nnouns + propernouns + nounss

	return nouns



def count_adjectives(argument):
	tagged = pos_tag(argument)
	#print tagged
	
	a1 = [word for word,pos in tagged if pos == 'JJ'] 
	a2 = [word for word,pos in tagged if pos == 'JJR']
	a3 = [word for word,pos in tagged if pos == 'JJS']
	
	adj = a1 + a2 + a3

	return adj


def count_verbs(argument):
	tagged = pos_tag(argument)
	#print tagged
	
	v1 = [word for word,pos in tagged if pos == 'VBG']  
	v2 = [word for word,pos in tagged if pos == 'VB']
	v3 = [word for word,pos in tagged if pos == 'VBD']
	v4 = [word for word,pos in tagged if pos == 'VBP'] 
	v5 = [word for word,pos in tagged if pos == 'VBN']
	v6 = [word for word,pos in tagged if pos == 'VBZ']
	
	verbs = v1 + v2 + v3 + v4 + v5 + v6
	
	return verbs


def count_adverbs(argument):
	tagged = pos_tag(argument)
	#print tagged
	
	a1 = [word for word,pos in tagged if pos == 'RB']  
	a2 = [word for word,pos in tagged if pos == 'RBR']
	a3 = [word for word,pos in tagged if pos == 'RBS']
	
	adj = a1 + a2 + a3

	return adj



def count_pronouns(argument):
	tagged = pos_tag(argument)
	#print tagged
	
	p1 = [word for word,pos in tagged if pos == 'PRP']  
	p2 = [word for word,pos in tagged if pos == 'PRP$']

	pron = p1 + p2 

	return pron



def average_freqdist(argument, debate):
	argument = set(argument)
	arg_length = len(argument)
	fdist = FreqDist(debate)
	chkr = SpellChecker("en_GB", debate)

	frequency = 0

	for w in argument:
		if chkr.check(w) == True:
			frequency = frequency + fdist[w]

	average_frequency = float(frequency) / arg_length

	return average_frequency



def split_bigrams(argument):

	bgs = nltk.bigrams(argument)
	bigrams =[]

	fdist = nltk.FreqDist(bgs)
	for k,v in fdist.items():
		bigrams.append(k)
	
	return bigrams



def split_trigrams(argument):

	bgs = nltk.trigrams(argument)

	trigrams = []

	fdist = nltk.FreqDist(bgs)
	for k,v in fdist.items():
		trigrams.append(k)
	
	return trigrams











