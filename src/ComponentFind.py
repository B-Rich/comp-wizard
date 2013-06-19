# ComponentFind.py
# Author: 
#
# CSCE 470 Project
# Project Title
# Sam, Sean, Erik
# Returns a list of components corresponding to user price range

import math, json, urllib, urllib2, time, sqlite3, os, sys
from operator import itemgetter

# output:
# Stores the database structure in a list
# Format: (Dictionary) Motherboard --> [(MOBO1), (MOBO2), ...]
# FIXED format (Title*, Price, ItemNumber, NewEgg ItemNumber*, ...)
def get_Database():
	database = {}
	conn = sqlite3.connect('../data/NewEggDatabase')
	cursor = conn.cursor()
	
	cursor.execute('select * from CD_Burners')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['CD_Burners'] = rows
	  
	cursor.execute('select * from CPU_Fans')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['CPU_Fans'] = rows
	
	cursor.execute('select * from Case_Fans')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['Case_Fans'] = rows
	
	cursor.execute('select * from Computer_Cases')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['Computer_Cases'] = rows
	
	cursor.execute('select * from Internal_HDD')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['Internal_HDD'] = rows
	
	cursor.execute('select * from Memory')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['Memory'] = rows
	
	cursor.execute('select * from Motherboards')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['Motherboards'] = rows
	
	cursor.execute('select * from Power_Supplies')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['Power_Supplies'] = rows
	
	cursor.execute('select * from Video_Cards')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['Video_Cards'] = rows
	
	cursor.execute('select * from Processors')
	rows = []
	for r in cursor:
	  rows.append(r)
	database['Processors'] = rows

	return database

# input: price range (1..5)
# output: Returns the average price to be conservative
def get_Price(price):
  # Price Ranges: (1) 400-700 (2) 701-900 (3) 901-1100 
  # (4) 1101-1400 (5) 1401-1700 (6) 1701+
  search_price = 0
  if price == 1:
    search_price = 550
  if price == 2:
    search_price = 800
  if price == 3:
    search_price = 1000
  if price == 4:
    search_price = 1250
  if price == 5:
    search_price = 1550
  if price == 6:
    search_price = 1800
  return search_price

# input: price range (1..5)
# output: upper bound on the range
def get_Max_Price(price):
  search_price = 0
  if price == 1:
    search_price = 700
  if price == 2:
    search_price = 800
  if price == 3:
    search_price = 1100
  if price == 4:
    search_price = 1400
  if price == 5:
    search_price = 1700
  if price == 6:
    search_price = 1000000 # no bound
  return search_price

# finds correct watts for PSU
def get_PSU(price, memory, database):
  # Power Supply Watts
  num_removed = 0
  for i in xrange(0, len(database['Power_Supplies'])):
    mother_watts = 50 + (100/5*(price-1))					# Motherboard (w/o CPU or RAM) 50W - 150W
    cpu_watts = 80 + (60/5*(price-1))						# Processor 80W - 140W
    GPU_watts = 50 											# AGP Video Card 30W - 50W --- PCI Express Video 100W - 250W --- Average PCI Card 5W - 10W
    HD_watts = 15 + (15/5*(price-1))						# Hard Drive 15W - 30W
    RAM = memory[4].split()[0]	# RAM 15W per 1GB
    if RAM == '2GB':
      RAM_watts = 30
    elif RAM == '3GB':
      RAM_watts = 45
    elif RAM == '4GB':
      RAM_watts = 60
    elif RAM == '6GB':
      RAM_watts = 75
    elif RAM == '8GB':
      RAM_watts = 120
    elif RAM == '12GB':
      RAM_watts = 180
    elif RAM == '16GB':
      RAM_watts = 240
    elif RAM == '24GB':
      RAM_watts = 360
    elif RAM == '32GB':
      RAM_watts = 480
    elif RAM == '64GB':
      RAM_watts = 960
    else:
      RAM_watts = 15        	 						
  
    total_watts = mother_watts + cpu_watts + GPU_watts + HD_watts + RAM_watts + 33  # Case/CPU Fans 3W (ea.) --- DVD/CD 20W - 30W  
    psu_watts = database['Power_Supplies'][i - num_removed][4]
    if psu_watts < total_watts * 1.2:
      database['Power_Supplies'].pop(i - num_removed)
      num_removed += 1

# input:
# input_price --> target price
# part_list --> List of components; format: [(Part1, Spec1, Spec2, ...), ..., (Part_N, ...)]
# output:
# Returns the Part that is closest to the target price as a tuple 
def get_Component(input_price, part_list):
  cmpr = 10000000
  best_price = ()
  best_rated = ()
  best_rated_list = []
  
  # Get closest priced part
  for p in part_list:
    price_diff = math.fabs(input_price - p[1])
    if price_diff < cmpr: # compares the closest price
      cmpr = math.fabs(input_price - p[1])
      best_price = p

  # Use the best_price part to get nearest two prices 
  # and then pick the highest rated
  price_sort = sorted(part_list, key=itemgetter(1))
  if len(price_sort) >= 3 and price_sort.index(best_price) + 1 < len(price_sort) and price_sort.index(best_price) - 1 >= 0:
    best_rated_list.append(price_sort[price_sort.index(best_price) - 1])
    best_rated_list.append(price_sort[price_sort.index(best_price)])

    best_rated_list.append(price_sort[price_sort.index(best_price) + 1])
    rating = -1.0
    for i in best_rated_list:
      if i[2] > rating:
        rating = i[2]
        best_rated = i
  else:
    best_rated = best_price

  return best_rated

# input:
# component database
# output:
# Returns the database with all non-compatible parts removed
def check_Compat(database, MOBO):

  # Processor Socket
  num_removed = 0
  for i in xrange(0, len(database['Processors'])):
    if MOBO[7] != database['Processors'][i - num_removed][7]:
      database['Processors'].pop(i - num_removed)
      num_removed += 1

  # Video_Cards Interface
  num_removed = 0
  for i in xrange(0, len(database['Video_Cards'])):
    if database['Video_Cards'][i - num_removed][9] == 'PCI Express 2.0 x16':
      if MOBO[11] == 'NULL':
        database['Video_Cards'].pop(i - num_removed)
        num_removed += 1
    if database['Video_Cards'][i - num_removed][9] == 'PCI Express x1':
      if MOBO[8] == 'NULL':
        database['Video_Cards'].pop(i - num_removed)
        num_removed += 1
    if database['Video_Cards'][i - num_removed][9] == 'PCI Slots':
      if MOBO[10] == 'NULL':
        database['Video_Cards'].pop(i - num_removed)
        num_removed += 1
  
  # Internal_HDD Interface
  num_removed = 0
  for i in xrange(0, len(database['Internal_HDD'])):
    if database['Internal_HDD'][i - num_removed][7] == 'SATA 3.0Gb/s':
      if MOBO[15] == 'NULL':
        database['Internal_HDD'].pop(i - num_removed)
        num_removed += 1
    if database['Internal_HDD'][i - num_removed][7] == 'SAS 6Gb/s':
      if MOBO[9] == 'NULL':
        database['Internal_HDD'].pop(i - num_removed)
        num_removed += 1
    if database['Internal_HDD'][i - num_removed][7] == 'SATA Raid':
      if MOBO[13] == 'NULL':
        database['Internal_HDD'].pop(i - num_removed)
        num_removed += 1

  """
  # Memory Speed
  print len(database['Memory'])
  num_removed = 0
  for i in xrange(0, len(database['Memory'])):
    if MOBO[12] != database['Memory'][i - num_removed][6]:
      database['Memory'].pop(i - num_removed)
      num_removed += 1
  print len(database['Memory'])
  """ 

  # Computer_Cases Size
  num_removed = 0
  for i in xrange(0, len(database['Computer_Cases'])):
    bMatch = 0
    compatibility = database['Computer_Cases'][i - num_removed][8].split()
    if MOBO[6] == 'Micro ATX':
      for type in compatibility:
        if type == 'Micro' or type == 'Micro-ATX' or type == 'microATX' or type == 'MicroATX':
          bMatch = 1
      if bMatch == 0:
        database['Computer_Cases'].pop(i - num_removed)
        num_removed += 1
    if MOBO[6] == 'ATX':
      for type in compatibility:
        if type == 'ATX':
          bMatch = 1
      if bMatch == 0:
        database['Computer_Cases'].pop(i - num_removed)
        num_removed += 1
  #print len(database['Computer_Cases'])

# removes components that are not compatible with video editing
def video_editing(database):

  # Memory must be 8 GB of RAM
  num_removed = 0
  for i in xrange(0, len(database['Memory'])):
    RAM = database['Memory'][i - num_removed][4].split()[0]
    if RAM != '8GB' and RAM != '12GB' and RAM != '16GB' and RAM != '24GB' and RAM != '32GB' and RAM != '64GB':
      database['Memory'].pop(i - num_removed)
      num_removed += 1

  # CPU must be at least i5 (~$189)
  num_removed = 0
  for i in xrange(0, len(database['Processors'])):
    if database['Processors'][i - num_removed][1] < 189:
      database['Processors'].pop(i - num_removed)
      num_removed += 1

  # GPU must be at least 2 GB
  num_removed = 0
  for i in xrange(0, len(database['Video_Cards'])):
    GPU_mem = database['Video_Cards'][i - num_removed][5].split()[0]
    if GPU_mem != '2GB' and GPU_mem != '2056MB' and GPU_mem != '3072MB' and GPU_mem != '4GB':
      database['Video_Cards'].pop(i - num_removed)
      num_removed += 1

# gaming requires 4GB
def gaming(database):

  # Memory must be 8 GB of RAM
  num_removed = 0
  for i in xrange(0, len(database['Memory'])):
    RAM = database['Memory'][i - num_removed][4].split()[0]
    if RAM != '4GB' and RAM != '6GB' and RAM != '8GB' and RAM != '12GB' and RAM != '16GB' and RAM != '24GB' and RAM != '32GB' and RAM != '64GB':
      database['Memory'].pop(i - num_removed)
      num_removed += 1

# input:
# price --> user specified price range
# output:
# Returns list of suitable components; 
# format: [(MOBO), (CPU), (GPU), (HD), (RAM), (PSU), (Case)] def search_price(price):
def search_price(price, component_database, type):
  price_range = get_Price(price)
  main_price = price_range - 40 # for fan and CD drive
  if type == 1:
    component_prices = [main_price * .15, main_price * .19, main_price * .20, main_price * .20, main_price * .05, main_price * .1, main_price * .11]
  elif type == 2:
    gaming(component_database)
    component_prices = [main_price * .13, main_price * .23, main_price * .28, main_price * .15, main_price * .04, main_price * .08, main_price * .09]   
  elif type == 3:
    video_editing(component_database)
    component_prices = [main_price * .13, main_price * .23, main_price * .28, main_price * .15, main_price * .04, main_price * .08, main_price * .09]   
  ordering = ['Motherboards', 'Processors', 'Video_Cards', 'Internal_HDD', 'Memory', 'Power_Supplies', 'Computer_Cases']
  components = []

  MOBO = get_Component(component_prices[0], component_database[ordering[0]])
  components.append(MOBO)
  check_Compat(component_database, MOBO)
  #print len(component_database['Internal_HDD'])

  for i in xrange(1, 5):
    components.append(get_Component(component_prices[i], component_database[ordering[i]]))
  get_PSU(price, components[4], component_database) # removes all PSU that correspond to appropriate RAM
  components.append(get_Component(component_prices[5], component_database[ordering[5]]))
  components.append(get_Component(component_prices[6], component_database[ordering[6]]))

  # get final price w/o GPU
  no_GPU_price = 0
  for i in xrange(0,len(components)):
    if i != 2:	# no GPU
      no_GPU_price += components[i][1]
  final_price = no_GPU_price + components[2][1]
  
  # pick cheaper GPU
  upper_bound = get_Max_Price(price)
  while final_price > upper_bound:
    component_database['Video_Cards'].remove(components[2])
    new_GPU = get_Component(component_prices[2], component_database['Video_Cards'])
    final_price = no_GPU_price + new_GPU[1]
    components.remove(components[2])
    components.insert(2, new_GPU)

  print "Total Price: "
  print final_price
  return components

def main():
  price = int(sys.argv[1])
  type = int(sys.argv[2])
  component_database = get_Database()
  components = search_price(price, component_database, type)

  # print title and NewEgg Item Number
  ordering = ['Motherboards', 'Processors', 'Video Cards', 'Internal Hard Drive', 'Memory', 'Power Supply', 'Cases']
  for i in xrange(0, len(components)):
    print ordering[i]
    print components[i][0]
    print components[i][1]

if __name__ == '__main__':
    main()


