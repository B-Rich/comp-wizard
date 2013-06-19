#UpdateDatabase.py
# Author: Samuel Collard
#
# CSCE 470 Project
# Project Title
# Sam, Sean, Erik
# Should be class that manages data base queries


import re, json, urllib, urllib2, time, sqlite3, os, GetReviews, classify


class DBManager:

  def __init__(self):
	self.classifier = classify.Classifier()

# read_specs(self, item_num)
# Takes in Newegg Item Number and looks up Tech Specs for that product

  def read_specs(self, item_num):
  	specs = {}
	  # GET the item based on item number
  	url = 'http://www.ows.newegg.com/Products.egg/'+str(item_num)+'/Specification'
  	request = urllib2.urlopen(url)
  	response = request.read()
  	data = json.loads(response)
    	  # data now has all sorts of info about the item
  	for spec in data['SpecificationGroupList']:	# There are 3 spec group lists we need to get specs from
    	  for pair in spec['SpecificationPairList']:	# Inside the spec group list they are organized as key value pairs
      	    specs[pair['Key']] = pair['Value']
  	return specs


# get_items(self, StoreID, CategoryID, SubCategoryID, NodeID, pageNum):
# Given which category you want to read it does an http post
# And reads all the products within a subcategory

  def get_items(self, StoreID, CategoryID, SubCategoryID, NodeID, pageNum):
	  # This takes a POST instead of a GET
  	url = "http://www.ows.newegg.com/Search.egg/Advanced"
  	data = {
    	  "IsUPCCodeSearch":      False,
    	  "IsSubCategorySearch":  True,
    	  "isGuideAdvanceSearch": False,
    	  "StoreDepaId":          StoreID,
    	  "CategoryId":           CategoryID,
    	  "SubCategoryId":        SubCategoryID,
    	  "NodeId":               NodeID,
    	  "BrandId":              -1,
   	  "NValue":               "",
    	  "Keyword":              "",
   	  "Sort":                 "FEATURED",
    	  "PageNumber":           pageNum
 	}
  	  # python way to do POST
  	params = json.dumps(data).replace("null", "-1")
  	request = urllib2.Request(url, params)
  	response = urllib2.urlopen(request)
  	data = json.loads(response.read())
		# in our case the only important thing is the list of products the search returns
  	return data['ProductListItems']

# updateCDBurners(self)
# Clears the CD_Burners table in the database and replaces it with new data
  def updateCDBurners(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	CD_Burners = ['DVD-ROM', 'CD-ROM', 'Brand', 'Interface', 'Type']
	#[('DVD-ROM', 'DVD'), ('CD-ROM', 'CD'), ('Brand', 'Brand'), ('Interface', 'Interface'), ('Type', 'Type')]
	sub = (u'CD / DVD Burners & Media', 10, u'CD_Burners', 5, 7589)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table CD_Burners')
	except: pass
	cursor.execute('create table CD_Burners (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, DVD TEXT, CD TEXT, Brand TEXT, Interface TEXT, Type TEXT)')
	try:
	  for i in range(10): # go through 10 pages, each page has 20 results
 	    products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in CD_Burners:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
	    	cursor.execute('insert into CD_Burners values (?,?,?,?,?,?,?,?,?)',args)	# add to database
	except: pass
	conn.commit()	# save changes

# updateComputer_Cases(self)
# Clears the Computer_Cases table in the database and replaces it with new data
  def updateComputer_Cases(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	Computer_Cases =  ['Brand', '80mm Fans', '120mm Fans', 'With Power Supply', \
		'Motherboard Compatibility','Internal 3.5" Drive Bays', '140mm Fans', \
		'Type', 'External 5.25" Drive Bays' ]
	sub = (u'Computer Cases', 9, u'Computer_Cases', 7, 7583)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table Computer_Cases')
	except: pass
	cursor.execute('create table Computer_Cases (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, Brand TEXT, Fans80 TEXT,\
		Fans120 TEXT, PowerSupply TEXT, MotherboardFormFactor TEXT, Internal3_5 TEXT,\
		Fans140 TEXT, Type TEXT, External5_25 TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in Computer_Cases:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Computer_Cases values (?,?,?,?,?,?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes



# updateCase_Fans(self)
# Clears the Case_Fans table in the database and replaces it with new data
  def updateCase_Fans(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	Case_Fans =  ['Fan Size', 'Brand', 'Power Connector', 'Type']
	#[ ('Fan Size', 'Size'), ('Brand', 'Brand'), ('Power Connector', 'PowerConnector'), ('Type', 'Type') ]
	sub = (u'Computer Cases', 9, u'Case_Fans', 573, 9248)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table Case_Fans')
	except: pass
	cursor.execute('create table Case_Fans (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, Size TEXT, Brand TEXT, PowerConnector TEXT, Type TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in Case_Fans:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Case_Fans values (?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes


# updateProcessors(self)
# Clears the Processors table in the database and replaces it with new data
  def updateProcessors(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	Processors =  ['Name', 'Brand', 'Multi-Core', 'CPU Socket Type', 'Operating Frequency', \
		'Cooling Device', 'L2 Cache', 'L3 Cache', 'Thermal Design Power']

	sub = (u'CPUs / Processors', 34, u'Processors', 343, 7671)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table Processors')
	except: pass
	cursor.execute('create table Processors (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, Name TEXT, Brand TEXT, \
		MultiCore TEXT, Socket TEXT, Frequency TEXT, Heatsink TEXT, \
		L2 TEXT, L3 TEXT, Power TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in Processors:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Processors values (?,?,?,?,?,?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes


# updateCPU_Fans(self)
# Clears the CPU_Fans table in the database and replaces it with new data
  def updateCPU_Fans(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	CPU_Fans =  ['Fan Size', 'Compatibility', 'Brand']

	sub = (u'CPUs / CPU_Fans', 34, u'CPU_Fans', 574, 12587)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table CPU_Fans')
	except: pass
	cursor.execute('create table CPU_Fans (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, Size TEXT, Compatibility TEXT, Brand TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in CPU_Fans:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into CPU_Fans values (?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes



# updateInternal_HDD(self)
# Clears the Internal_HDD table in the database and replaces it with new data
  def updateInternal_HDD(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	Internal_HDD =  ['Capacity', 'Brand', 'Cache', 'Interface', 'RPM', 'Form Factor']

	sub = (u'Hard Drives', 15, u'Internal_HDD', 14, 7603)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table Internal_HDD')
	except: pass
	cursor.execute('create table Internal_HDD (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, Capacity TEXT, Brand TEXT, Cache TEXT, Interface TEXT, RPM TEXT, FormFactor TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in Internal_HDD:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Internal_HDD values (?,?,?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes



# updateMemory(self)
# Clears the Memory table in the database and replaces it with new data
  def updateMemory(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	Memory =  ['Capacity', 'Brand', 'Speed', 'Type']

	sub = (u'Memory', 17, u'Memory', 147, 7611)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table Memory')
	except: pass
	cursor.execute('create table Memory (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, Capacity TEXT, Brand TEXT, Speed TEXT, Type TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in Memory:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Memory values (?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes




# updateIntel_Motherboards(self)
# Clears the Intel_Motherboards table in the database and replaces it with new data
  def updateIntel_Motherboards(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	Intel_Motherboards =  ['Brand', 'CPU Type', 'Form Factor', 'CPU Socket Type', 'PCI Express x1', 'SATA 6Gb/s', 'PCI Slots', 'PCI Express 2.0 x16', \
		'Memory Standard', 'SATA RAID', 'eSATA', 'SATA 3Gb/s', 'Power Pin']

	sub = (u'Motherboards', 20, u'Intel_Motherboards', 280, 7627)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	#try: cursor.execute('drop table Intel_Motherboards')
	#except: pass
	#cursor.execute('create table Intel_Motherboards (Title TEXT, Price REALRating REAL, NewEggItemNumber TEXT, Brand TEXT, CPU_Type TEXT, Form_Factor TEXT, Socket TEXT, PCIe_x1 TEXT, SATA_6gbs TEXT, \
	#	PCI TEXT, PCIe_x16 TEXT, Memory TEXT, SATA_RAID TEXT, eSATA TEXT, SATA_3gbs TEXT, Power_Pin TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in Intel_Motherboards:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Motherboards values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes



# updateAMD_Motherboards(self)
# Clears the AMD_Motherboards table in the database and replaces it with new data
  def updateAMD_Motherboards(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	AMD_Motherboards =  ['Brand', 'CPU Type', 'Form Factor', 'CPU Socket Type', 'PCI Express x1', 'SATA 6Gb/s', 'PCI Slots', 'PCI Express 2.0 x16', \
		'Memory Standard', 'SATA RAID', 'eSATA', 'SATA 3Gb/s', 'Power Pin']

	sub = (u'Motherboards', 20, u'AMD_Motherboards', 280, 7627)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]

	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in AMD_Motherboards:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Motherboards values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes

# Wrapper function to update motherboards
  def updateMotherboards(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	try: cursor.execute('drop table Motherboards')
	except: pass
	cursor.execute('create table Motherboards (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, Brand TEXT, CPU_Type TEXT, Form_Factor TEXT, Socket TEXT, PCIe_x1 TEXT, SATA_6gbs TEXT, \
		PCI TEXT, PCIe_x16 TEXT, Memory TEXT, SATA_RAID TEXT, eSATA TEXT, SATA_3gbs TEXT, Power_Pin TEXT)')
	conn.commit()
	self.updateAMD_Motherboards()
	self.updateIntel_Motherboards()
		
		
		
# updatePower_Supplies(self)
# Clears the Power_Supplies table in the database and replaces it with new data
  def updatePower_Supplies(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	Power_Supplies =  ['Maximum Power', 'Type', 'PCI-Express Connector', 'Brand', 'SATA Power Connector', 'Main Connector', 'Connectors', 'Modular']
		#initialize the subcategory
	sub = (u'Power Supplies', 32, u'Power_Supplies', 58, 7657)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table Power_Supplies')
	except: pass
	cursor.execute('create table Power_Supplies (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, Power REAL, Type TEXT, PCIe TEXT, Brand TEXT, SATA TEXT, Main_Connector TEXT, Connectors TEXT, Modular TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
		
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in Power_Supplies:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
		# Turning Power into integer
		ex = re.compile("[0-9]*W")
		s = ex.search(str(args[4]))
		Power = s.group()
		args[4] = int(Power[:-1])
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Power_Supplies values (?,?,?,?,?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes




# updateVideo_Cards(self)
# Clears the Video_Cards table in the database and replaces it with new data
  def updateVideo_Cards(self):
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	  # list of features we want to keep track of
	Video_Cards =  ['DVI', 'Memory Size', 'Brand', 'Max Resolution', 'Chipset Manufacturer', 'Interface', 'GPU', 'Power Connector', 'Core Clock']

		#initialize the subcategory
	sub = (u'Video Cards & Video Devices', 38, u'Video_Cards', 48, 7709)
	category = sub[0]
     	catID = sub[1]
     	subcat = sub[2]
     	subcatID = sub[3]
     	nodeID = sub[4]
		# delete and recreate table
	try: cursor.execute('drop table Video_Cards')
	except: pass
	cursor.execute('create table Video_Cards (Title TEXT, Price REAL, Rating REAL, NewEggItemNumber TEXT, DVI TEXT, Memory TEXT, Brand TEXT, Max_Resolution TEXT, Manufacturer TEXT, Interface TEXT, GPU TEXT, Power_Connector TEXT, Core_Clock TEXT)')
	for i in range(10): # go through 10 pages, each page has 20 results
 	  products = self.get_items(1, catID, subcatID, nodeID, int(i+1))
	  try:
	    for p in products:
		try: rating = GetReviews.Rate(p['NeweggItemNumber'], self.classifier)
		except: rating = 0.0
	      	args = [p["Title"], float(p["FinalPrice"][1:]), rating, p['NeweggItemNumber']] # add name and price, Item Number
	      	specs = self.read_specs(p['ItemNumber'])
	    	for feature in Video_Cards:	# only keep the features we want
	    	  try: args.append(specs[feature])
		  except: args.append('NULL')
	    	#print 'Adding ',args
			# add to database
	    	cursor.execute('insert into Video_Cards values (?,?,?,?,?,?,?,?,?,?,?,?,?)',args)	
	  except: pass
	conn.commit()	# save changes



def main():

  start = time.time()
  print 'Loading Database'
  db = DBManager()
  print 'Updating CDBurners'
  db.updateCDBurners()
  print 'Updating Computer_Cases'
  db.updateComputer_Cases()
  print 'Updating Case_Fans'
  db.updateCase_Fans()
  print 'Updating Processors'
  db.updateProcessors()
  print 'Updating CPU_Fans'
  db.updateCPU_Fans()
  print 'Updating Hard Drives'
  db.updateInternal_HDD()
  print 'Updating Memory'
  db.updateMemory()
  print 'Updating Motherboards'
  db.updateMotherboards()
  print 'Updating Power Supplies'
  db.updatePower_Supplies()
  print 'Updating Video Cards'
  db.updateVideo_Cards()

  end = time.time()
  print '\n\nUpdating took ',int((end-start)/60.0),'mins',int(end-start)%60,'secs'

  print 'classifier stats are: ',db.classifier.stats()



if __name__ == '__main__':
    main()


