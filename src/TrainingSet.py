# TrainingSet.py
# Builds and stores the training set

import pickle, GetReviews, data, Tokenizer, classify, math

# BuildTrainingSet()
# Massive function used to construct the training set
def BuildTrainingSet():
	# initialize variables
  database = data.getDatabase()
  IDF = dict(pickle.load(open('../data/idf.pickle','rb')))
  numReviews = 0
  posReview = {}
  numPos = 0
  negReview = {}
  numNeg = 0
		# For each product in each subcategory
  for table in database:
    for product in database[table]:
	item = product[3]
	revs = GetReviews.readReview(item)["Reviews"]
		# get the review
	try:
	  for r in revs:
	    if (numReviews%37)==0:	# Analyze every 37th review
	  	tf = {}
		  # Get reviews for you to read
	  	con = r['Cons']
	  	pro = r['Pros']
	  	comment = r['Comments']
		  # Read the reviews
	  	print pro,' :: ',con,' :: ',comment
		  # set up to add to training set
	  	con = Tokenizer.stemming(Tokenizer.tokenize(r['Cons']))
	  	pro = Tokenizer.stemming(Tokenizer.tokenize(r['Pros']))
	  	comment = Tokenizer.stemming(Tokenizer.tokenize(r['Comments']))
		  # Treat all parts as one review
	  	for token in list(con+pro+comment):
		  if token in tf: tf[token] = tf[token] + 1
		  else: tf[token] = 1
	  	for t in tf:
		    # tf-idf formula
	    	  tf[t] = float(1+math.log(tf[t]))*IDF[t]
		    # hopefully you have had time to read, now decide
	    	Q = int(raw_input('\n1 for good.... 0 for bad.....\n').rstrip('\n'))
	    	if Q==1:	# Good
		  posReview[numPos] = tf	# add to training set
		  numPos = numPos + 1
		elif Q==0:	# Bad
		  negReview[numNeg] = tf	# add to training set
		  numNeg = numNeg + 1
		else: print 'FAIL!!!!!!'

	    numReviews = numReviews + 1		# increase number of reviews
	except: pass
  saveSet(posReview,negReview)	# Save the training sets
  return (numPos, numNeg)



# Use python pickle function to save the training sets
def saveSet(posSet,negSet):
  pickle.dump(dict(posSet),open('../data/PicklePos','wb'))
  pickle.dump(dict(negSet),open('../data/PickleNeg','wb'))

# Use python pickle function to load the training sets
def loadSet():
  posSet = dict(pickle.load(open('../data/PicklePos','rb')))
  negSet = dict(pickle.load(open('../data/PickleNeg','rb')))
  return (posSet,negSet)

def main():
  #d = raw_input('Are you Ready?!\n\n')
  #BuildTrainingSet()
  (pSet,nSet) = loadSet()

  print pSet
  print nSet

if __name__ == '__main__':
    main()


