import sys
import nltk


if len(sys.argv) != 2:
	print "Usage: python main.py <filename>"
	sys.exit(0)

print(nltk.pos_tag(nltk.word_tokenize(sys.argv[1])))
