#FUNCTIONS FOR INDIVIDUAL ARGUMENTS

import nltk,re
from nltk.tokenize import word_tokenize, sent_tokenize
from wordlists import*  #for keywords
from badwords import*
from abbreviations import*
from collections import Counter
from nltk.tag import pos_tag
from enchant.checker import SpellChecker



#keywordcount
def linkingwordcount(argument_raw):

	argument = argument_raw.lower()
	
	linking_words = explanation + additional + contrast + proviso + example + importance + other + result + quotes + conclusion
	numWords = len(argument.split())

	d = dict((i, argument.count(i)) for i in linking_words)
	keyWordCounter = sum(d.values())

	percentKeywords = (float(keyWordCounter) / numWords)

	return percentKeywords

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


def badwordcount(argument_raw):
	
	argument = argument_raw.lower()
	numWords = len(argument.split())

	d = dict((i, argument.count(i)) for i in bad_words)
	badwordCounter = sum(d.values())

	outcome = (float(badwordCounter) / numWords)

	return outcome

#grammar
def spellCheck(argument): 
	#print argument
	words =  len(argument)
	abbr = abb1 + abb2 + abb3
	#print words

	errors = 0                             
	chkr = SpellChecker("en_GB", argument)
	#print chkr
	#chkr.set_text(argument)

	argument = re.sub("[^\w\d'\s]+", " ", argument)
	print argument
	argument = argument.split()

	for word in argument:
		if chkr.check(word) == False:
			errors+=1
			#print word
			#print errors
			if (chkr.check(word.upper()) == True) or (chkr.check(word + ".") == True or (word in abbr)):
				errors-=1                                    #and check in abbreviation list!
				print errors


	outcome = (float(errors) / words)

	return outcome


def punctCount(argument):
	counts = Counter(argument)
	punctuation = '?!'
	punct_count ={k: v for k, v in counts.iteritems() if k in punctuation}

	sumP = sum(punct_count.values())
	sentences = len(nltk.sent_tokenize(argument))

	outcome = (float(sumP) / sentences)


	return outcome

def containsHyperlink(argument):
	links = re.findall(r'(https?://[^\s]+)', argument)
	return len(links)

def capsCount(argument_raw):

	#argument = argument_raw.lower()
	capwords = 0

	argument = re.sub("[^\w\d'\s]+", " ", argument_raw)  #removes everything apart from apostrophe
	#print argument
		
	for word in nltk.word_tokenize(argument):
		if word == word.upper():
			print word
			capwords +=1

	#ABBREVIATION TEST!

	numWords = len(argument.split())
	percentCapwords = (float(capwords) / numWords)
	print percentCapwords


	return percentCapwords

#def namedEntities(argument):



arg1 = '''It goes against human nature and, as other fellow voters have mentioned, the definition of "Marriage". And you can't exclude religion from this argument, because thats what happened when people don't have faith or belief in any religion. Religion is there to act as guidelines to what is right and what is wrong. Religion is a way of life. Without it, we're lost.'''
arg2 = '''Two men/women together does not seem natural. Although we know the world is changing and there are new ideas the purpose of two humans being together is to reproduce and make new life. Marriage is in front of God and the words are taken from the Bible but it is obvious that God does not approve of this so doesn't it seem ironic in a way?'''
arg3 = '''Is incestual marriage right or wrong? Does gay marriage include incestual homosexual marriage? Which country legalized homosexual unions which lead to a lower marriage rate?'''
arg4 = '''Marriage evolved because of moral and religious grounds rather than a mere union approved by the state... To debase marriage just to accomodate base desires of gay couples in disguise if a right is simply stupid...'''
arg5 = '''Marriage is between a man and a woman. It has always been so. If two people want to live in Sin together, I have no problem with that. However, they shouldn't be rewarded with tax breaks. And I sure don't want them to have a platform to spew their garbage and cram it down my kids' throat. Since Homosexuality is a learned sin (think about it) I don't want my kids to learn that it is ok. This public exposure/support of the homosexuals isn't good for morality, and if morality goes, then so does society. (Lord of the Flies)'''
arg6 = '''From a religious standpoint gay marriage isn't even possible. Let along right. But everyone isn't religious or adheres to specific religious guidance.'''
arg7 = '''Marriage is defined as between a woman and a man. So the word "marriage" may be misused in this case. Civil unions, well that's a different matter.'''
arg8 = '''The Marriage issue should be out of politicians and lawmakers. Marriages are for the Church to decide, Congress have no power to pass a legislation forcing religious institutions about marriage. Maybe, if the courts were to allow gay marriage, it would be alright since it is not a religious institution, it doesn't break the Separation between Church and State ruled by the Supreme Court.'''
arg9 = '''I did not propose "separate but equal." I proposed "distinct and different." Man/woman relationships, especially in the aggregate, have a very different set of implications than man/man and woman/woman relationships. If the law is to contemplate man/woman relationships intelligently, it has to be able to isolate them. A law requiring separate schools and public accomodations for homosexual people would violate "separate but equal." Law defining marriage as a man/woman relationship does not'''
arg10 = '''Here is a reason why gay marriage could be wrong. If gay marriage is ok, then sister and brother marriage is ok too? Whats the difference? Oh wait, the sex is the difference, so SISTER and SISTER or BROTHER and BROTHER is ok... right?'''
arg11 = '''The real issue is - why is the government involved in this issue at all? We take a personal, religious institution and regulate it, then the government comes back and wants to redefine it. It should not be a political issue, because my personal, religious things should be separate from government regulation. Marriage and the government should not mix. That solves the "problem".'''
arg12 = '''I am a christian. The bible says plain out that homosexuality is wrong. Call me pathetic, weak, or whatever you want to call me, but I know for sure that the bible is the TRUTH, the WHOLE truth, and the ONLY truth.'''
arg13 = '''To me gay marriage is wrong. I respect other opinions but to me it is an unnatural way and against my moral law.'''
arg14 = '''Gay marriage is wrong. God made man and a woman to populate the earth. How can human species survive if they are only attracted to their same sex? Obviously, not.'''
arg15 = '''Guys AND Girls were made for a reason. This reason is not so they can pair up with the same sex. It is so that they can pair up with opposite genders. Opposites Attract, Every where, wether its in magnets, electricity, atoms, or humans. Besides, it just doesnt work with two guys (genitals), thats why there are female reproductive systems and male reproductive systems. They only work together, so there is only one way to reproduce.. Guy AND Girl!'''
arg16 = '''gays are overrated. it is another "look at me" stunt. i think gays are the product of overly protective parents, abuse, or liberal wakoness (it should be a disease). if you gays would stop calling attention to yourselves, nobody would really care what you do'''
arg17 = '''EVERYONE, regardless of sexual orientation, has the right to be miserable. I say let gay people know the joys of divorce, splitting of assets, custody, alimony, child support, the whole nine yards! In fact, make civil unions illegal; it makes it too easy to "walk away" from a relationship and encourages roomates to be "couples" to help a buddy out with benefits.Civil Unions, gone, Gay marraige, IN!'''
arg18 = '''Do gay marriages hurt anyone? No. Do gay marriages kill many people? No. Are gay marriages going to end the world? No. Are gay marriages in anyway affecting anyone but the two getting married? No. Then why the hell do straight ppl get so offensive? If you want marrage to just be between you fine let them do something else to show they love each other. Bottom line, if you love someone you should be allowed to be with them. God accepts everyone, his people should follow that. Bottom line, it should be a sin to kep two people who love each other apart. Enough said.'''
arg19 = '''I don't care if calling it "marriage" offends people, or violates what they call the sanctity of marriage, gays should have the same RIGHTS that a married couple gets. Civil Union, Marriage, the coming together of two souls, or whatever you prefer to call it- gays NEED to be recognized on that level. Not allowing this is a violation to the constitution and it's unfortunate that the Supreme Court won't take a case on this because they're leaving it up to the states, yet Bush wanted to make an amendment stating what marriage is...'''
arg20 = '''Yes I believe gay marriage should be allowed. Mosy who do not want it to be allowed just dont like homosexuality all together, and therefore the opposing side tends to be prejudice. If two men or two women are happy together, love each other, and want to be with each other forever why shouldn't they be allowed to get married??'''
arg21 = '''There is an argument of people saying is gay marriage acceptable or unacceptable. I would say most of the population of Britain would say it is wrong however I think anybody should be allowed to express there feelings to the one they love so I think it is acceptable. Because how come we can get married to the other secuality however a man can't express his feelings to a man or a woman and a woman as gay sexuality I think gays should be allowed to do what they like when they like !!'''
arg22 = '''Gay marriage is a lifestyle choice. It may be considered "unnatural", but that is between that person and his/her love interest. Love is all some people have... You can't take that one given right away because it makes you uncomfortable. They want acceptance and understanding. Let them be happy or just ignore it. You don't chose to be gay either. Who would chose to live that way? They are constantly being harrassed and can't be with their loved one. It's unfortunate and cruel. Please be respecful of them. They have done nothing wrong, God created them that way.'''
arg23 = '''Religion, lifestyle etc is a personal choice. If your religion or culture disallows gay marriage, that's fine. It means you don't want to marry a person of the same gender. But then why should it extend to other religions or cultures? Gay people marrying in no way affects your marriage to the opposite gender either, they simply get married and get on with it just like you do.'''
arg24 = '''How can anyone say that Gay Marriage is Wrong. It is a personal choice that is made from personal beliefs so who are we to say that gay couples do not have the right to enjoy all of the benefits that straight couples do?'''
arg25 = '''The Bible is not the origin of marriage. Marriage is found in almost every society, including those that were never touched by Christianity (or Judaism) and societies that preceded Christianity (and Judaism). The Bible can only be argued to be the origin of Christian marriage, and even that is difficult to prove.'''
arg26 = '''Why does it matter? If two people regardless of gender love each other to the point of which the two marry, shouldn't that follow what the bible really teaches us. All you bible nutjobes by the way are making me sick. The bible teaches love and forgiveness, and lets not forget dont judge others before you judge yourself.'''
arg27 = '''It might be against the teachings of the bible etc... but only because a gay relationship bears no offspring which is why it was banned. Also it was seen to weaken the position of men. Time have changed... its time to accept.'''
arg28 = '''This idea is essentially playing with semantics. Most people who are against gay marriages are really against gays, so calling it a "civil union" might shut their mouth, but will still not satisfy them. Furthermore, the effects on society are bound to be minimal on an overpopulated Earth where global warming will drastically reduce the already overtaxed ability of Nature to feed us.And if "undermining the assumptions of law that has developed over hundreds of years" is really an issue, than law should never change. We should revert back to tribes & slavery - why challenge any assumption?'''
arg29 = '''I think it all depends on the individualist's point of view. We have no right to go against it. Different people have different point of views.We perceive that Gay marriage is weird and disgusting but they might feel the same way as we do and find that Man and Women marriages are weird. So I think it all depends on perceptions and we have no whats so ever right to question one's perceptions. We humans are very selfish creatures we only view things according to what we think is right and those who go against it we think that they are wrong'''
arg30 = '''If you do not like gay marriage and thing it is wrong then do not watch a gay couple make out.Who are you to tell people that their veiws are incorrect and that they must change there feelings and that apparently they are wrong. Meanwhile, everyone is entitled to their opinions, but keep them to yourself. Do not try to change others based on your beliefs. It is selfish and takes away self rights.'''
arg31 = '''AS LONG AS IT IS NOT DISEASE WE SHOULD ALL BE FINE WITH ITT ITS NOT OUR BUSINESS!!!'''
arg32 = '''Gays are human beings just like we are. They should have the right to marriage just like we are.'''

linking = linkingwordcount(arg1)
readability = ColemanLiauIndex(arg1)
badwords = badwordcount(arg1)
grammar = spellCheck(arg1)
punct = punctCount(arg1)
links = containsHyperlink(arg1)
caps = capsCount(arg1)
print "percentage linking words", linking
print "readabality", readability
print "percentage badwords", badwords
print "percentage mistakes", grammar
print "!/? relative to sentences", punct
print "hyperlinks", links
print caps