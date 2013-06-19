
import json, urllib, urllib2, time, sqlite3, os

def getDatabase():
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
	
	
	
if __name__ == '__main__':
    main()
