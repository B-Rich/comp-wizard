#  GetReviews.py
#  Samuel Collard
#
#  Functions that deal with getting the reviews from Newegg
#  Calculates the ratings Quotient based on 
#  number of reviews, std deviation, and classifer score


import json, urllib, urllib2, time, sqlite3, os, math


# readReview(item_num)
# Performs an http GET request for the given item and returns the json dictionary
def readReview(item_num):
  specs = {}
  	# GET the item's reviews based on item number
  url = 'http://www.ows.newegg.com/Products.egg/'+str(item_num)+'/Reviews'
  request = urllib2.urlopen(url)
  response = request.read()
  data = json.loads(response)
  #print data['PaginationInfo']
   	  # data now has reviews for the item
  return data


# numReviewScore(n)
# Given the total numbers of reviews, n,
# return a score indicating quality of reviews	
def numReviewScore(n):
  if n==0:
	return 0.0
  elif n<10:
	return 0.1
  elif n<25:
	return 0.2
  elif n<50:
	return 0.3
  elif n<75:
	return 0.4
  elif n<100:
	return 0.5
  elif n<250:
	return 0.6
  elif n<500:
	return 0.7
  elif n<750:
	return 0.8
  elif n<1000:
	return 0.9
  else:
	return 1.0

# Review numbers are returned as xx,xxx
# Need to remove commas and return as an integer
def stringToNum(num):
  Num = ''
  for i in num.split(','):
    Num = Num + i
  return int(Num)



# standardDeviationScore(dat,avg,total)
# Computes the standard deviation of the review scores
# inputs are the ProductReviewBarInfo, average rating, and number of ratings
def standardDeviationScore(dat,avg,total):
  stdDev = 0.0
	# get number of people who rated 1, 2, 3, 4, or 5 stars
  num1 = stringToNum(dat['Rating1Count'])
  num2 = stringToNum(dat['Rating2Count'])
  num3 = stringToNum(dat['Rating3Count'])
  num4 = stringToNum(dat['Rating4Count'])
  num5 = stringToNum(dat['Rating5Count'])
  	# calculate standard deviation of reviews to the average
  stdDev = math.sqrt( (num1*(avg-1)*(avg-1) + num2*(avg-2)*(avg-2) + num3*(avg-3)*(avg-3) + \
	num4*(avg-4)*(avg-4) + num5*(avg-5)*(avg-5))/total)
		# smaller the standard deviation the higher the score
  if stdDev<0.5:
	return 1.0
  elif stdDev<1:
	return 0.75
  elif stdDev<2:
	return 0.5
  else:
	return 0.25



# Rate(ItemNum, classifier)
# Given the product to rate and a classifer
# Calculates the rating quotient, and final Rating of the product
# Based on a 5 star scale
def Rate(ItemNum, classifier):

  rq = 0.0
	# get the Review, average rating and number of reviews
  review = readReview(ItemNum)
  avgRating = int(review['Summary']['Rating'])
  numReviews = stringToNum(review['Summary']['TotalReviews'])

    # Calculate the Rating Quotient
  rq =  0.4 * numReviewScore(numReviews) + \
	0.4 * standardDeviationScore(review['ProductReviewBarInfo'],avgRating,numReviews) + \
	0.2 * classifier.classify(ItemNum)

  	# Final rating is average rating multiplied by rating quotient
  return float(avgRating*rq) 


  


def main():
  pass


  
	
if __name__ == '__main__':
    main()
