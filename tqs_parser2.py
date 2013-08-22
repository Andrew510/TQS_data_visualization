#tqs_parser2.py
#Author: Andrew A. Campbell
#IN: path of directory containing a single day of data from TQS
#OUT: 
#  two files for each unique user recorded that day
#  One combines location tracks and activity points
#  Other file combines logs of BART and Muni trips

import sys
import re
import csv
import os


#1 - UNIQUE USER NAMES
def unique_names(dir):
	filenames = os.listdir(dir) #list of file names in the directory
	usernames=[]
#open each file and extract any new user names that are not in the usernames[] list
	for name in filenames: 
		f=open(name,'rU')
		table = csv.reader(f)
		table.next()
		for row in table:
			if row[1] not in usernames:
				usernames.append(row[1])
		f.close()		
	return usernames 

#2 - WRITE THE COMBINED ACTIVITIES/TRACKS FILES
def activitiy_tracks(date,usernames):
	#date is the prefix for each file name. It is also the folder name. Has form YYYY-MM-DD
	#usernames are the unique user names for that date
		
	#2.1 - create a new file for each unique user
	
	head = ['id','username','long','lat','pointtime','starttime','endtime','type','icon'] #header for output csv tables
	
	for name in usernames:
		new_file_name = name+'_'+date+'_ActsTracks.csv' #new file name for each unique usersname
		new_file = open(new_file_name,'wb') #opens new file
		table = csv.writer(new_file,dialect='excel') #creates csv object for each new file
		table.writerow(head)	
		
		#2.1.2 - read through activity files and pass values to output files		
		f_acts = open(date+'_activities.txt','rU')
		acts = csv.reader(f_acts)
		acts.next() #skips the header row
		for row in acts:			
			if row[1] == name:
				match=re.search(r'(-\d+\.\d+)\s+(\d+\.\d+)',row[2])
				table.writerow([row[0],name,match.group(1),match.group(2),'',row[3],row[4],'activity','red_circle'])
		f_acts.close()
		
		#2.1.3 - read through the rawdata files and pass values to output files
		f_trax = open(date+'_rawdata.txt','rU')
		trax = csv.reader(f_trax)
		trax.next() #skips the header row
		for row in trax:			
			if row[1] == name:
				match=re.search(r'(-\d+\.\d+)\s+(\d+\.\d+)',row[2])
				table.writerow([row[0],name,match.group(1),match.group(2),row[3],'','','track','small_green'])
		f_trax.close()
		
	new_file.close()

#3 - WRITE THE COMBINED BART/MUNI TRIP FILES	
def bartmuni_trips(date,usernames):
	#3.1 create a new file for each unique user
	head = ['id','username','on_stop','off_stop','on_time','off_time','route_long_name','vehicle_id','mode'] #header for output csv tables
	for name in usernames:
		new_file_name = name+'_'+date+'_BART_Muni.csv' #new file name for each unique usersname
		new_file = open(new_file_name,'wb') #opens new file
		table = csv.writer(new_file,dialect='excel') #creates csv object for each new file
		table.writerow(head)
		
	#3.1.2 - read through BART files and pass data to appropriate output
		f_BART = open(date+'_bart.txt','rU')
		bart_trips = csv.reader(f_BART)
		bart_trips.next() #skips the header row
		for row in bart_trips:			
			if row[1] == name:				
				table.writerow([row[0],name,row[2],row[3],row[4],row[5],'','','BART'])
		f_BART.close()
		
	#3.1.3 - read through the Muni files and pass data to output files
		f_Muni = open(date+'_Muni.txt','rU')
		Muni_trips = csv.reader(f_Muni)
		Muni_trips.next() #skips the header row
		for row in Muni_trips:			
			if row[1] == name:				
				table.writerow([row[0],name,row[2],row[3],row[4],row[5],row[6],row[7],'Muni'])
		f_Muni.close()
		
		
	new_file.close()
	
	
def main():
	if len(sys.argv[1:]) > 1:
			print 'Error: Takes only one argument as input: the file path to the directory of TQS data'
			
	current_dir = sys.argv[1]
	os.chdir(current_dir) #makes sure runs in correct directory, regardless of where opened
	
	#finds the date of the data, which is also directory name
	dir_date=re.search(r'\d+-\d+-\d+',current_dir).group()
	
	#returns a list of unique usernames for the date
	unames = unique_names(current_dir)
	
	#builds the combined track and activity files
	activitiy_tracks(dir_date,unames)
	
	#build combined BART and Muni trip log
	bartmuni_trips(dir_date,unames)
		

if __name__ == '__main__':
  main()