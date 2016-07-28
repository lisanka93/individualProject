


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

	





