import re

test = "''''kkk !!!  ''"

debate = re.sub("[^\w\d'\s]+", "", test)   #deletes punctuation 

print debate