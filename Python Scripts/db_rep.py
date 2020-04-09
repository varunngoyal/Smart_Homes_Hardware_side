import paho.mqtt.client as mqtt
import time
import threading
import configparser
import json
from pymongo import MongoClient 
from bson.json_util import dumps
import csv
import datetime
## mongoexport -d mqtt_raspi -c temp1 --pretty -o temp2

 #from array import *

######################################################################################
#------------------ALL THE CONFIGURATIONS---------------------------------------------
######################################################################################

config = configparser.ConfigParser()
config.read('raspy.properties')



# Database credentials
mongo_database_name = config.get('mongo', 'mongo.database')
mongo_port_no = int(config.get('mongo', 'mongo.port_no'))
mongo_host = config.get('mongo', 'mongo.host')

#######################################################################################
#Listen to clients who want to configure themselves
mongoclient = MongoClient(mongo_host, mongo_port_no)
mydb = mongoclient[mongo_database_name]
mydb.temp1.drop()

def parsetoJson(message_string):
	try:
		parsed_json = json.loads(message_string)
		return parsed_json
	except Exception as x:
		print('Error parsing json message: {0}'.format(type(x).__name__))

for x in mydb.temp.find():
	y = x#parsetoJson(dumps(x))
	y['start']=int(y['start'])
	y['end']=int(y['end'])

	start1=y['start']
	end1=y['end']
	w1=y['watt']
	#print(start1)
	#print(end1)
	for i in range(0,6):
		y['_id'] = "A"
		y['watt']=float(w1)
		del y['_id']
		#print("i is ",i)

		dt = datetime.datetime.utcfromtimestamp((10*3600*24*i + (int(start1))))
		iso_format = dt.isoformat() + 'Z'
		#m11=("ISODate("+ iso_format+")")
		y['start'] ="ISODate("+ iso_format+")"

		dt = datetime.datetime.utcfromtimestamp((10*3600*24*i + (int(end1))))
		iso_format = dt.isoformat() + 'Z'
		y['end'] = "ISODate("+ iso_format+")"


		#print(y)
		k = mydb.temp1.insert_one(y)  ##dont know why it was inserting record twice
		#print('Printing k', k)



