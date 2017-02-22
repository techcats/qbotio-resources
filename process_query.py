# Author: Kenny Iraheta
# Org: TechCats
# Date: 1.29.2017

import nltk
import string

user_query = input("Enter your question: \n")
user_query = user_query.lower()

print ("\nYou have entered: " + user_query + "\n")

#tokenize query
tokens = nltk.word_tokenize(user_query)
print ("Tokenized Words: \n")
print (tokens)

#tag query
tagged = nltk.pos_tag(tokens)
print ("\nTagged Words: \n")
print (tagged)

#identify kind of entities
entities = nltk.chunk.ne_chunk(tagged)
print ("\nGroup Words: \n")
print (entities)

#get stopwords
stopwords = nltk.corpus.stopwords.words('english')

#remove stopwords from query -- query ready for db
db_query = list(set(tokens) - set(stopwords))
print ("\nQuery minus stop words: \n")
print (db_query)
