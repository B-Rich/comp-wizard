#  classify.py
#  Samuel Collard
#
#  Class and Methods used by the KNN classifier
#  calculates Cosine Similarity of tf-idf vectors
#  comparing Product Reviews to the Training Set


import math, pickle, GetReviews, data, Tokenizer, TrainingSet

# CosineSim(q,d)
# Finds the cosine similarity between dictionaries q and d
# Inputs: two dictionaries with the Key being a stemmed token
#	and Value is the tf-idf score 
# Outputs: The cosine similarity ranging from -1 to 1
def CosineSim(q,d):
	# Need floats
  dot = 0.0
  magQ = 0.0
  magD = 0.0
  qK = q.keys()
  dK = d.keys()
  keys = list(set(qK) & set(dK)) # find intersection of keys
  for k in keys:	# dot product only matters if both have a common term
	dot = dot + q[k]*d[k]
  for a in q:		# Sum all terms squared
	magQ = magQ + q[a]*q[a]
  for b in d:		# Sum all terms squared
	magD = magD + d[b]*d[b]
		# Formula for Cosine Similarity
  cos = float(dot)/float(math.sqrt(magQ)*math.sqrt(magD))
  return cos


# def idf()
# Calucates the idf scores for every product currently in the database
# Returns a dictionary where the key is the term and the value is the idf score
def idf():
  IDF = {}
  numDocs = 0
	# Get all the products from the database
  dat = data.getDatabase()
  for table in dat:
    #print '.'
	# Go through each product in each table
    for product in dat[table]:
	item = product[3]
		# Get their reviews
	revs = GetReviews.readReview(item)["Reviews"]
	try:
	  for r in revs:
	    #print r
		# Tokenize and Stem reviews
	    con = Tokenizer.stemming(Tokenizer.tokenize(r['Cons']))
	    pro = Tokenizer.stemming(Tokenizer.tokenize(r['Pros']))
	    comment = Tokenizer.stemming(Tokenizer.tokenize(r['Comments']))
	    #print 'Before:',r['Cons'],'\n\nAfter:',con
		# Count unique tokens in the document
	    for token in list(set(con) | set(pro) | set(comment)):
		if token in IDF: IDF[token] = IDF[token] + 1
		else: IDF[token] = 1
	  numDocs = numDocs + 1
		# Increment the number of documents
	except: pass
		# Calculate and return the idf score
  for term in IDF:
    IDF[term] = math.log(float(numDocs)/float(IDF[term]))
  pickle.dump(dict(IDF),open('../data/idf.pickle','wb'))  # Pickling saves SOOO much time
  return IDF



# tf_idf()
# Creates a dictionary with the Key being each NewEggItemNumber in the database
# with the value bing a list of each review associated with that product
# each element in the list is a dictionary containing stemmed tokens and tf-idf scores
# Yes... a dictionary of lists of dictionaries. What are you gonna do?
def tf_idf():
  TF_IDF = {}
	# Load the inverse document frequencies
  IDF = idf()
  #IDF = dict(pickle.load(open('idf.pickle','rb')))
  dat = data.getDatabase()	# get all of the products
  for table in dat:
    print '.'	# progress marker
    for product in dat[table]:	# For each product in each table
	item = product[3]	# Item number is [3] in the tuple
	revs = GetReviews.readReview(item)["Reviews"]	# we want to read the actual reviews
	product_review = []
	try:
	  for r in revs:	# for each review
	    tf = {}
		# Tokenize and stem the entire review
	    con = Tokenizer.stemming(Tokenizer.tokenize(r['Cons']))
	    pro = Tokenizer.stemming(Tokenizer.tokenize(r['Pros']))
	    comment = Tokenizer.stemming(Tokenizer.tokenize(r['Comments']))
		# combine pros, cons, and comments sections
	    for token in list(con+pro+comment):		# calculate the term frequencies
		if token in tf: tf[token] = tf[token] + 1
		else: tf[token] = 1
	    for t in tf:
	    	tf[t] = float(1+math.log(tf[t]))*IDF[t] # calculate tf-idf score

	    product_review.append(tf)	# add to list of reviews
	except: pass
	TF_IDF[item] = product_review	# add list of reviews to the dictionary
  return TF_IDF



# class to classify reviews into quality reviews or poor reviews
class Classifier:

  def __init__(self):
	self.TF_IDF = tf_idf()
	(p,n) = TrainingSet.loadSet()
	self.pos = p
	self.neg = n
	self.numP = 0
	self.numN = 0
	print '..Loaded.. '
# KNN(self, review)
# Given a review it finds the K nearest neighbors in the training set
# if closer to the positive reviews, return 1
# if closer to the negative reviews, return 0
  def KNN(self, review):
    k = 3		# 5 nearest neighbors
    sim_list = []
    #print 'Review inside KNN =',review
    for p in self.pos:	# compare all quality reviews
	#print 'p = ',p
	sim = abs(CosineSim(dict(review),dict(self.pos[p])))
	sim_list.append((1,sim))
    for n in self.neg:	# compare all poor reviews
	sim = abs(CosineSim(dict(review),dict(self.neg[n])))
	sim_list.append((0,sim))
		# Sort the list
    sim_list = sorted(sim_list, key=lambda x: x[1], reverse=True) #sort by similarity
    Sum = 0
    for i in range(k):	# get number of quality reviews
	Sum = Sum + sim_list[i][0]
    if Sum>int(k/2):	# if more than half of k are good
	return 1  # Quality
    else:
	return 0  # Poor

# classify(self, NewEggItemNumber)
# Takes a product and returns the percent of quality reviews
  def classify(self, NewEggItemNumber):
    review_list = self.TF_IDF[NewEggItemNumber]	# get all them reviews
    Sum = 0
    for review in review_list: # classify each review
	#print 'review of',NewEggItemNumber,'is: ',review
	Sum = Sum + self.KNN(review)	# Sum increase if review is quality
    self.numP = self.numP + Sum
    self.numN = self.numN + len(review_list) - Sum
    return float(Sum)/float(len(review_list))	#return percent of quality reviews

  def stats(self):
    return (self.numP, self.numN)

def main():
  print 'initializing'
  c = Classifier()
  print c.classify('N82E16822136075')

if __name__ == '__main__':
    main()






