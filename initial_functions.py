import nltk,re
import nltk.grammar
from nltk.tree import *
from wordlists import*
from badwords import*
import enchant, string
from enchant.checker import SpellChecker
import RAKE
import operator
from nltk.corpus import stopwords, nps_chat
from collections import Counter
from textblob import TextBlob
from nltk.tree import ParentedTree
from nltk.corpus import stopwords, treebank, wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag, tnt


def features(argument):
	print "linking words: ", linkingwordcount(argument)
	print "readability: ", ColemanLiauIndex(argument)
	print "vulgar language: ", badwordcount(argument)
	print "grammar: ", spellCheck(argument)
	print "aggressiveness: ", capsCount(argument)
	print "punctuation: ", punctCount(argument)
	print "links: ", containsHyperlink(argument)
	print "----------------------------------------------------------------------------------"
	print "keywords: ", keywordextraction(argument)
	print "blob_nounphrases: ", nounphrases(argument)
	print "all nouns", all_nouns(argument)
	print "___________________________________________________________________________________"
	#preprocess(argument)
	return
"""MAKE STES OUT OF ALL LISTS much faster in python!"""


def linkingwordcount(argument_raw):

	argument = argument_raw.lower()
	
	linking_words = explanation + additional + contrast + proviso + example + importance + other + result + quotes + conclusion
	numWords = len(argument.split())


	defaultPercentage = 0.03           # at least 5 percent of an argument should be keywords

	d = dict((i, argument.count(i)) for i in linking_words)
	keyWordCounter = sum(d.values())

	percentKeywords = (float(keyWordCounter) / numWords)


	if percentKeywords >= defaultPercentage:
		passed1 = True
		return "contains 3 percent linking words"
	else:
		passed1 = False
		return "contains less than 3 percent linking words"


def ColemanLiauIndex(argument):

	letters = len(argument)

	sentences = len(nltk.sent_tokenize(argument))

	words =  len(nltk.word_tokenize(argument))
	
	outcome = (5.879851 * letters / words - 29.587280 * sentences / words - 15.800804)
	#print outcome
	if outcome > 13:
		return "failed readability"
	else:
		return "argument is readable"

def badwordcount(argument_raw):
	
	argument = argument_raw.lower()

	d = dict((i, argument.count(i)) for i in bad_words)
	badwordCounter = sum(d.values())

	if badwordCounter > 2:
		return "contains insulting language"
	else:
		return "no insulting language"
		

def spellCheck(argument):
	words =  len(nltk.word_tokenize(argument))

	errors = 0                             
	chkr = SpellChecker("en_GB")
	chkr.set_text(argument)

	for err in chkr:
		errors+=1

	for word in argument:
	
	bool_word = chkr.check(word)
	if bool_word == False:
		if (chkr.check(word.upper()) == True) or (chkr.check(word + ".") == True):
			errors-=1         #and check in abbreviation list!


	#print errors
	if ((float(errors) / words) > 0.07):
		return "contains too many grammatical errors"
	else:
		return "grammar good"

		#https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines




def capsCount(argument_raw):

	argument = argument_raw.lower()

	argument = re.sub("[^a-zA-Z]", " ", argument)  
		
	for word in nltk.word_tokenize(argument):
		if word == word.upper():
			#print word
			capwords +=1

	numWords = len(argument.split())
	percentCapwords = (float(capwords) / numWords)
	#print percentCapwords

	defaultPercentage = 0.1

	if percentCapwords >= defaultPercentage:
		passed1 = True
		return "too many caps"
	else:
		passed1 = False
		return "not aggressive (caps)"

	
	#think of a way to count consecutive caps words, when does it sound aggressive?
	#exclude abbreviations!!!


def punctCount(argument):
	counts = Counter(argument)
	punctuation = '?!'
	punct_count ={k: v for k, v in counts.iteritems() if k in punctuation}

	sumP = sum(punct_count.values())
	sentences = len(nltk.sent_tokenize(argument))

	if sumP > (sentences*2):
		return "too many ?/! (aggressive)"
	else:
		return "good punctuation"


def containsHyperlink(argument):
	links = re.findall(r'(https?://[^\s]+)', argument)
	return len(links)


def keywordextraction(argument):
	rake_object = RAKE.Rake("SmartStoplist.txt")

	keywords = rake_object.run(argument)

	return keywords
"""
	for item in keywords:
		if item[1] >= 4.0:
			print item[0]"""



def nounphrases(argument):
	tb = TextBlob(argument)
	return tb.noun_phrases

def all_nouns(argument_raw):

	argument = argument_raw.lower()
	argument = re.sub("[^a-zA-Z]", " ", argument) 
	
	tagged_sent = pos_tag(argument.split())
	
	with open('SmartStoplist.txt', 'r') as myfile:
		data=myfile.read().replace('\n', ' ')
		data=data.split()

	print " ----------------------------------------------------------tagged normal "
	print tagged_sent

	print "----------------------------------------------------------- tagged chat"
	print tagged_sent2
	
	meaningful_words = [w for w in tagged_sent if not w in data] 

	propernouns = [word for word,pos in meaningful_words if pos == 'NNP']
	nouns = [word for word,pos in meaningful_words if pos == 'NN']
	nounss = [word for word,pos in meaningful_words if pos == 'NNS']

	nouns = nouns + propernouns + nounss
	return nouns
	print nounss






def preprocess(document):
	#tokanizing sentence and applying part of speech tags
	sentences = nltk.sent_tokenize(document)
	#print sentences
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	#print sentences
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	sen = [val for sublist in sentences for val in sublist]   #flatten
	#print sen

	#pos_tags = [pos for (token, pos) in nltk.pos_tag(sen)]
	#print pos_tags
	
	#print sentences
	#noun-phrase chunking:
	grammar = r"""
		NP: {<CC>?<RB>?<DT|JJ|NN.*>+}
		# Chunk sequences of DT, JJ, NN
		PP: {<IN><NP>}
		# Chunk prepositions followed by NP
		VP: {<PRP\$>?<VB.*><PRP\$>*<NP|PP>+} # Chunk verbs and their arguments
			{<NP><VB.*><RB>*}				
	""" 

	cp = nltk.RegexpParser(grammar)
	result = cp.parse(sen)
	
	#return result
	print result
	print result.leaves()
	#result.draw()

	





