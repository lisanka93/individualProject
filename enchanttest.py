import nltk
from enchant.checker import SpellChecker
from nltk.tokenize import word_tokenize, sent_tokenize




chkr = SpellChecker("en_GB")

word ="blubb hdsa hdas dksad"
print word.capitalize()

print chkr.check(word)

print word.split()

print nltk.word_tokenize(word)



