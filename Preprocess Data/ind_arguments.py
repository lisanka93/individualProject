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
from collections import Counter
from nltk.probability import FreqDist


#counts linkingwords in a post - should normalise it
def linkingwordcount(argument):
	
	linking_words = explanation + additional + contrast + proviso + example + importance + other + result + quotes + conclusion
	#sentences = len(nltk.sent_tokenize(argument))

	d = dict((i, argument.count(i)) for i in linking_words)
	keyWordCounter = sum(d.values())
	#print "here", d

	#percentKeywords = (float(keyWordCounter) / sentences)

	#return percentKeywords
	return keyWordCounter

#readability
def ColemanLiauIndex(argument):

	tokenized = word_tokenize(argument)
	#print tokenized
	
	argument_no_punct = [w for w in tokenized if w.isalpha()]
	stringI = ' '.join(w for w in argument_no_punct)
	#print stringI

	letters = len(stringI)
	#print "letter", letters

	sentences = len(nltk.sent_tokenize(argument))
	#print sentences

	words =  len(argument_no_punct)
	#print "words", words
	
	outcome = (5.879851 * letters / words - 29.587280 * sentences / words - 15.800804)

	return outcome


def badwordcount(argument):

	numWords = len(argument)

	d = dict((i, argument.count(i)) for i in bad_words)
	badwordCounter = sum(d.values())

	#outcome = (float(badwordCounter) / numWords)

	#return outcome
	return badwordCounter

#grammar
def spellCheck(argument): 

	words =  len(argument)
	abbr = abb1 + abb2 + abb3
	#print words

	errors = 0                             
	chkr = SpellChecker("en_GB", argument)

	for word in argument:
		if chkr.check(word) == False:
			errors+=1
			#print word
			#print errors
			if (chkr.check(word.upper()) == True) or (chkr.check(word.capitalize()) == True) or (chkr.check(word + ".") == True or (word in abbr)):
				errors-=1                                    #and check in abbreviation list!
				#print errors


	outcome = (float(errors) / words)

	return outcome


def punctCount(argument):

	counts = Counter(argument)
	punctuation = '?!.'                         #include fullstop?
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

	#print "argument without linK", argument
	return len(links)

def capsCount(argument):

	#argument = argument_raw.lower()
	capwords = 0
		
	for word in argument:
		if word == word.upper() and len(word) > 1:
			#print word
			capwords +=1

	#ABBREVIATION TEST!

	numWords = len(argument)
	percentCapwords = (float(capwords) / numWords)


	return percentCapwords

def preprocess_for_nee_and_print_ind(argument):                        #need to write better function that might correct the sentence first before extracting them but for now it will do it
	

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
	#print entities
	#named_entities = [w for w in entities if w.lower() not in mcl]
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
	#print debate
	
	tagged = pos_tag(argument)
	
	propernouns = [word for word,pos in tagged if pos == 'NNP']  #should be able to make or statement no?
	nnouns = [word for word,pos in tagged if pos == 'NN']
	nounss = [word for word,pos in tagged if pos == 'NNS']
	
	nouns = nnouns + propernouns + nounss

	return nouns



def count_adjectives(argument):
	tagged = pos_tag(argument)
	#print tagged
	
	a1 = [word for word,pos in tagged if pos == 'JJ']  #should be able to make or statement no?
	a2 = [word for word,pos in tagged if pos == 'JJR']
	a3 = [word for word,pos in tagged if pos == 'JJS']
	
	adj = a1 + a2 + a3

	return adj




def count_verbs(argument):
	tagged = pos_tag(argument)
	#print tagged
	
	v1 = [word for word,pos in tagged if pos == 'VBG']  #should be able to make or statement no?
	v2 = [word for word,pos in tagged if pos == 'VB']
	v3 = [word for word,pos in tagged if pos == 'VBD']
	v4 = [word for word,pos in tagged if pos == 'VBP']  #should be able to make or statement no?
	v5 = [word for word,pos in tagged if pos == 'VBN']
	v6 = [word for word,pos in tagged if pos == 'VBZ']
	
	verbs = v1 + v2 + v3 + v4 + v5 + v6
	
	return verbs



def count_adverbs(argument):
	tagged = pos_tag(argument)
	#print tagged
	
	a1 = [word for word,pos in tagged if pos == 'RB']  #should be able to make or statement no?
	a2 = [word for word,pos in tagged if pos == 'RBR']
	a3 = [word for word,pos in tagged if pos == 'RBS']
	
	adj = a1 + a2 + a3

	return adj



def count_pronouns(argument):
	tagged = pos_tag(argument)
	#print tagged
	
	p1 = [word for word,pos in tagged if pos == 'PRP']  #should be able to make or statement no?
	p2 = [word for word,pos in tagged if pos == 'PRP$']

	pron = p1 + p2 

	return pron




def average_freqdist(argument, debate):

	#take lemmatised argument and lemmatised debate and add all dist together ad divide by number of words in argument
	#takes tokenized argument (lemma_sent)
	argument = set(argument)
	arg_length = len(argument)
	fdist = FreqDist(debate)
	chkr = SpellChecker("en_GB", debate)

	frequency = 0

	for w in argument:
		if chkr.check(w) == True:
			frequency = frequency + fdist[w]
			#print w, fdist[w]

	average_frequency = float(frequency) / arg_length

	return average_frequency

















"""


arg1 = '''It goes against human nature and, http://ww.blubb  as other fellow voters have mentioned, the definition of "Marriage". And you can't exclude religion from this argument, because thats what happened when people don't have faith or belief in any religion. Religion is there to act as guidelines to what is right and what is wrong. Religion is a way of life. Without it, we're lost.'''


linking = linkingwordcount(arg1)
readability = ColemanLiauIndex(arg1)
badwords = badwordcount(arg1)
grammar = spellCheck(arg1)
punct = punctCount(arg1)
links = containsHyperlink(arg1)
caps = capsCount(arg1)
namedE = preprocess_for_nee_and_print(arg1)
print "percentage linking words", linking
print "readabality", readability
print "percentage badwords", badwords
print "percentage mistakes", grammar
print "!/? relative to sentences", punct
print "hyperlinks", links
print "caps", caps
print "named E", namedE
"""