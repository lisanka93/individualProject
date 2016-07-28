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

###########################################################      PREPROCESSING      ##########################################################################
#preprocessing debate:
def preprocess_debateI(debate):

	#setting everything to lower to make processing easier
	debate = debate.lower() 

	#finding and counting hyperlinks, then delete them from debate (otherwise influence data)
	links = re.findall(r'(w?w?w?.?https?://[^\s]+)', debate)

	#return number of hyperlinks in debate
	x = len(links)

	if x != 0:
		for link in links:
			debate = debate.replace(link, '')
	
	#deleting all punctuation apart from apostrophes
	debate = re.sub("[^\w\d'\s]+", " ", debate)
	debate = debate.split()
	return (debate, x)                                     #returns tokenized debate


def preprocess_debateII(debate):
	
	#removing stopwords
	with open('SmartStoplist.txt', 'r') as myfile:
		data=myfile.read().replace('\n', ' ')
	
	data=data.split()

	meaningful_words = [w for w in debate if not w in data and w.isalpha()]
	#print meaningful_words
	return meaningful_words                         #returns list of debate words - stopwords

############################################################################################################################

def lemmatised_words(debate):	
	
	lemmatised_words = [lemma(w) for w in debate]
	#print lemmatised_words

	fdist = FreqDist(lemmatised_words)

	list_mc = fdist.most_common(20)

	most_common_lemmatised_list = []
	
	for list_tuple in list_mc:
		most_common_lemmatised_list.append(list_tuple[0].encode('utf-8'))

	return most_common_lemmatised_list

#stemming using snowball stemmer
def stemmed_snowball(debate):

	snowball = SnowballStemmer("english")

	stemmed_words_snowball = [snowball.stem(w) for w in debate]

	fdist2 = FreqDist(stemmed_words_snowball)
	list_mc2 = fdist2.most_common(20)

	most_common_snowball = []
	
	for list_tuple in list_mc2:

		most_common_snowball.append(list_tuple[0].encode('utf-8'))

	return most_common_snowball


########################################################## most common nouns ##############################################################################

def extract_nouns(debate):
	#print debate
	
	tagged = pos_tag(debate)
	
	propernouns = [word for word,pos in tagged if pos == 'NNP']  #should be able to make or statement no?
	nnouns = [word for word,pos in tagged if pos == 'NN']
	nounss = [word for word,pos in tagged if pos == 'NNS']
	
	nouns = nnouns + propernouns + nounss

	c = Counter(nouns)
	most_common_nouns = c.most_common(20)
	mcn_list = []
	for list_tuple in most_common_nouns:
		mcn_list.append(list_tuple[0])
	
	return mcn_list

##########################################################    unusual stems   ##################################################################

def unusual_words(text, mcs, google):    
    text = text.split()

    #take text
    # spellcheck it
    # put correct words in list
    # stem them
    #check if word stem in one of the lists
    #return list of stems not in google list
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
    
    return unusual_words                    #will miss words that are not in the enchant checker dictionary!!!!!! 



######################################################## named entity #########################################################

#if there is time i want to train a classifier, now its really bad

def preprocess_for_nee_and_print(argument, mcl):                        #need to write better function that might correct the sentence first before extracting them but for now it will do it
	

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
	#print entities
	#named_entities = [w for w in entities if w.lower() not in mcl]
	named_entities = set(named_entities)
	named_entities = list(named_entities)
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