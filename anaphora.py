import nltk

prp_thing = {"IT"}
prp_third_person = {"HE", "HIM", "SHE", "HER", "THEY", "THEM"}
prp_third_person_possessive = {"HIS", "HERS", "THEIRS"}
punctuation = {".", "!", "?"}

def anaphora(text):
	return simple_anaphora(text)

# This function parses a text and attempts to perform anaphora resolution. 
# It traverses the pos-tagged tree and looks for named entities using NLTK.
# Makes the naive assumption that each personal pronoun (PRP-tag) is referring to the most recent named entity.
def simple_anaphora(text):
	text_sent   = nltk.sent_tokenize(text)
	text_sentences = []

	most_recent_person = None
	most_recent_thing  = None
	for sentence in text_sent:
		text_tokens = nltk.word_tokenize(sentence)
		text_tagged = nltk.pos_tag(text_tokens)
		text_ne = nltk.ne_chunk(text_tagged, False)

		words_in_sentence = []
		for i in range(0, len(text_ne)):
			word = text_ne[i]
			if is_person(word):
				most_recent_person = word[0]
			elif is_thing(word):
				most_recent_thing = word[0]
			else:
				anaphor = is_anaphor(word)
				if anaphor != None:
					if most_recent_person != None:
						if anaphor == "PERSON":
							words_in_sentence.append(most_recent_person[0])
							continue
						elif anaphor == "PERSON$":
							words_in_sentence.append(most_recent_person[0])
							words_in_sentence.append("'")
							words_in_sentence.append("s")
							continue
					elif most_recent_thing != None and anaphor == "THING":
						words_in_sentence.append(most_recent_thing[0])
						continue
			words_in_sentence.append(str(text_tokens[i]))
		text_sentences.append(words_in_sentence)

	return text_sentences

def is_person(word):
	try:
		if word.label() == "PERSON":
			return True
	except AttributeError:
		return False
	return False

def is_thing(word):
	try:
		if word.label() == "GPE":
			return True
	except AttributeError:
		return False
	return False

def is_anaphor(word):
	try:
		if word[1] == "PRP":
			if word[0].upper() in prp_thing:
				return "THING"
			elif word[0].upper() in prp_third_person:
				return "PERSON"
		elif word[1] == "PRP$":
			if word[0].upper() in prp_third_person_possessive:
				return "PERSON$"
	except AttributeError:
		return None
	return None