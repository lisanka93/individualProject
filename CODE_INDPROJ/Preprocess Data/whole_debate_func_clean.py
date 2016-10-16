#whole debate functions clean

import nltk,re
from not_ne_list import *
from ten_google_stem_list import*
from twen_google_stem_list import*
#from nltk.tokenize import word_tokenize 
from nltk.probability import FreqDist
#from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.tag import pos_tag
from collections import Counter
from pattern.en import lemma, singularize
from enchant.checker import SpellChecker
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.collocations import *



###########################################################      PREPROCESSING      ##########################################################################
#preprocessing debate:

def preprocess_debateI(debate):
	"""sets everything to lower case and removes hyperlinks in order to avoid spelling mistakes. after finding
		and counting all hyperlinks also deletes all punctuation and returns tokanized debate / list"""

	debate = debate.lower() 

	links = re.findall(r'(w?w?w?.?https?://[^\s]+)', debate)

	x = len(links)

	if x != 0:
		for link in links:
			debate = debate.replace(link, '')

	debate = re.sub("[^\w\d'\s]+", "", debate)   
	debate = debate.split()
	return (debate, x)                                 


def preprocess_debateII(debate):
	"""removes all stopwords and returns list of most meaningful words in debate"""
	
	with open('SmartStoplist.txt', 'r') as myfile:
		data=myfile.read().replace('\n', ' ')
	
	meaningful_words = [w for w in debate if not w in data and w.isalpha()]

	return meaningful_words                         #returns list of debate words - stopwords



def preprocess_debateIII(debate):      #lemmatises text
	lemmatised_words = [lemma(w) for w in debate]

	return lemmatised_words




#############################################bigrams   & trigrams     #################################################
	
def bigram_extr(meaningful_words):             

	mc_bigrams = []

	bgs = nltk.bigrams(meaningful_words)
	fdist = nltk.FreqDist(bgs)
	for k,v in fdist.items():
		if v > 5:
			mc_bigrams.append(k)

	return mc_bigrams

def trigram_extr(meaningful_words):


	mc_trigrams = []

	bgs = nltk.trigrams(meaningful_words)
	fdist = nltk.FreqDist(bgs)
	for k,v in fdist.items():
		if v > 5:
			mc_trigrams.append(k)

	return mc_trigrams


######################################################## long words ####################################################################


def long_words(debate):                                   #long words in debate

	lemmatised_words = debate

	long_words = [w for w in lemmatised_words if len(w) > 9]
	long_words = set(long_words)

	long_words_correct = []
	chkr = SpellChecker("en_GB", debate)                   #spellchecking

	for word in long_words:
		if chkr.check(word) == True:
			long_words_correct.append(word.encode('utf-8'))

	return long_words_correct                              #returns list of long words


def very_rare_long_words(debate, longwords):             #takes lemmatised debate and the long words and checks which one has a frequency distribution of 1

	fdist = FreqDist(debate)
	chkr = SpellChecker("en_GB", debate)

	very_rare = []

	for w in longwords:
		if fdist[w] < 2 and chkr.check(w) == True:
			very_rare.append(w.encode('utf-8'))

	return very_rare

###########################################################################################################################################



def lemmatised_words(debate):	
	
	lemmatised_words = debate

	fdist = FreqDist(lemmatised_words)

	list_mc = fdist.most_common(20)

	most_common_lemmatised_list = []
	
	for list_tuple in list_mc:
		if list_tuple[1] > 5:           
			most_common_lemmatised_list.append(list_tuple[0].encode('utf-8'))

	return most_common_lemmatised_list


def stemmed_snowball(debate):

	snowball = SnowballStemmer("english")

	stemmed_words_snowball = [snowball.stem(w) for w in debate]

	fdist2 = FreqDist(stemmed_words_snowball)
	list_mc2 = fdist2.most_common(20)             #adjust this too!!!

	most_common_snowball = []
	
	for list_tuple in list_mc2:
		if list_tuple[1] > 5:
			most_common_snowball.append(list_tuple[0].encode('utf-8'))

	return most_common_snowball



########################################################## most common nouns ##############################################################################

def extract_nouns(debate):

	
	tagged = pos_tag(debate)

	
	propernouns = [word for word,pos in tagged if pos == 'NNP']  
	nnouns = [word for word,pos in tagged if pos == 'NN']
	nounss = [word for word,pos in tagged if pos == 'NNS']
	
	nouns = nnouns + propernouns + nounss

	c = Counter(nouns)
	most_common_nouns = c.most_common(5)          
	mcn_list = []
	for list_tuple in most_common_nouns:
		if list_tuple[1] > 5:
			mcn_list.append(list_tuple[0])
	
	return mcn_list


##########################################################    unusual stems   ##################################################################

def unusual_words(text, mcs, google):    
    text = text.split()


    spellC = SpellChecker("en_GB")
    correct_words = []

    for w in text:
    	if w.isalpha():
    		correct = spellC.check(w)
    		if correct == True:
    			correct_words.append(w.encode('utf-8'))

    snowball = SnowballStemmer("english")

    delete_list = mcs + google

    stemmed_words = [snowball.stem(w) for w in correct_words]
    unusual_words = [w.encode('utf-8') for w in stemmed_words if w not in delete_list]
    unusual_words = set(unusual_words)
    unusual_words = list(unusual_words)
    
    return unusual_words                 



######################################################## named entity #########################################################

#if there is time i want to train a classifier, now its really bad

def preprocess_for_nee_and_print(argument):                    	

	sentences = nltk.sent_tokenize(argument)
	tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

	entity_names = []

	for tree in chunked_sentences:
		#tree.draw()
		entity_names.extend(extract_entity_names(tree))

	#print entity_names
	named_entities = [w for w in entity_names if w not in not_NE]

	return named_entities

def extract_entity_names(tree):
    entity_names = []

    if hasattr(tree, 'label') and tree.label:
        if tree.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in tree]))
        else:
            for child in tree:
                entity_names.extend(extract_entity_names(child))

    return entity_names