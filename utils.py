import numpy as np
import math
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from scipy import spatial

# stopwords
stopwords = set(stopwords.words('italian'))

# from https://stackoverflow.com/questions/21030391/how-to-normalize-array-numpy
def normalized(a, axis=-1, order=2):
	l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
	l2[l2==0] = 1
	return a / np.expand_dims(l2, axis)

# cleaning stuff
def preprocessing_nltk(e):
	ps = PorterStemmer()

	e = e.lower().replace('\n', '')
	e = word_tokenize(e)
	e = [w for w in e if w.isalpha()]
	e = [w for w in e if not w in stopwords]
	e = [ps.stem(w) for w in e]
	return e

def compute_tfidf(word_freq, n_words_doc, n_docs, n_docs_with_word):
	tf = word_freq / n_words_doc
	idf = math.log10(n_docs / n_docs_with_word)
	return tf * idf

def cosine_similarity(vec_src, vec_tgt):
	return 1 - spatial.distance.cosine(vec_src, vec_tgt)

def tfidf_inverse_index(voc2doc, doc2voc):

	# inverse index
	voc2doc_tfidf = {}

	# doc2voc_tfidf
	doc2voc_tfidf = {}

	# create inverse index with tfidf
	for w, docs in voc2doc.items():
		
		# skip in case we already have a word in the vocabulary
		if w in voc2doc_tfidf.keys(): continue
		
		# empty list (of future tuples)
		voc2doc_tfidf[w] = []
		
		# for each document that contains w
		for d in docs:
			
			# create an empty structure if it's the first match
			if not d in doc2voc_tfidf.keys():
				doc2voc_tfidf[d] = {}
			
			# get document words (all its words)
			content = doc2voc[d]
			
			# compute tfidf
			tfidf = compute_tfidf(content.count(w), len(content), len(doc2voc.keys()), len(docs))
			
			# fill the vector
			voc2doc_tfidf[w].append((d, tfidf))
			doc2voc_tfidf[d][w] = tfidf

	return {
		'voc2doc_tfidf': voc2doc_tfidf,
		'doc2voc_tfidf': doc2voc_tfidf
	}