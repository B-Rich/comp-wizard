#{u'product': {u'description': u'Intel Core i7 Quad-Core i7-2600K 3.4GHz Desktop Processor:Clock Speed: 3.', u'language': u'en', u'author': {u'name': u'Walmart', u'accountId': u'1113342'}, u'gtins': [u'00735858217361'], u'country': u'US', u'brand': u'Intel', u'title': u'Intel Core I7 Quad-core I7-2600k 3.4ghz Desktop Processor', u'creationTime': u'2011-10-17T19:24:41.000Z', u'modificationTime': u'2011-10-19T20:27:28.000Z', u'link': u'http://www.walmart.com/ip/Intel-Core-i7-Quad-Core-i7-2600K-3.4GHz-Desktop-Processor/16472580?sourceid=1500000000000003142050&ci_src=14110944&ci_sku=16472580', u'condition': u'new', u'images': [{u'link': u'http://i.walmartimages.com/i/p/00/73/58/58/21/0073585821736_500X500.jpg'}], u'gtin': u'00735858217361', u'inventories': [{u'shipping': 2.9700000000000002, u'price': 328.98000000000002, u'availability': u'inStock', u'channel': u'online', u'currency': u'USD'}], u'googleId': u'7082117731464506749'}, u'kind': u'shopping#product', u'id': u'tag:google.com,2010:shopping/products/1113342/7082117731464506749', u'selfLink': u'https://www.googleapis.com/shopping/search/v1/public/products/1113342/gid/7082117731464506749?alt=json'}



import json, urllib2
  # The only thing you change to search for something different is the 'q=...'
  # but make sure it is url-encoded, ie: no spaces
q = 'https://www.googleapis.com/shopping/search/v1/public/products?key=AIzaSyAukIhwv-eCHfl26Glxi_RlEU3l4zREnLM&country=US&q=intel+i7&alt=json'
  # alt=json at the end can be changed to alt=atom when viewing in a browser


req = urllib2.urlopen(q)
resp = req.read()

data = json.loads(resp)

  # taken from what json returns in commented example above
for item in data['items']:
  print item['product']['title']
  print item['product']['inventories'][0]['price']
  print item['product']['link']
  


#items
#-product

#--description
#--language
#--author
#--gtins
#--country
#--brand
#--title			!!
#--creationTime
#--modificationTime
#--link				!!
#--condition
#--images
#--gtin
#--inventories
#---[0]
#----price			!!
#--googleId


