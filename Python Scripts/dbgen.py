import paho.mqtt.client as mqtt
import time
import threading
import configparser
import json
from pymongo import MongoClient 
from bson.json_util import dumps
import csv

## mongoexport -d mqtt_raspi -c temp --pretty -o temp

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
mydb.temp.drop()
i=0


##hall

with open('csv files/tubelight1.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "tubelight", "time": "10", "topic": "1001", "start": "0", "end": "0", "message": "ON",
					  "from": "user_name", "watt": "40", "duty_cycle": "98", "category": "actuator", "ack_val": "null","room":"hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])/40 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i=i+1

with open('csv files/tubelight2.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "tubelight", "time": "10", "topic": "1002", "start": "0", "end": "0", "message": "ON",
					  "from": "user_name", "watt": "40", "duty_cycle": "98", "category": "actuator", "ack_val": "null","room":"hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])/40 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/fan1.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "fan", "time": "5", "topic": "2001", "start": "0", "end": "0", "message": "ON",
				"from": "user_name", "watt": "80", "duty_cycle": "95", "category": "actuator", "ack_val": "null",
				"room": "hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*15 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/fan2.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "fan", "time": "5", "topic": "2002", "start": "0", "end": "0", "message": "ON",
				"from": "user_name", "watt": "80", "duty_cycle": "95", "category": "actuator", "ack_val": "null",
				"room": "hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*15 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port1.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4001", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*50 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port2.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4002", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*50 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port3.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4003", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*16 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port4.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4004", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*60 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/television.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x ={"type" : "television", "time" : "6", "topic" : "3001", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"50","duty_cycle":"90", "category":"actuator", "ack_val": "null","room": "hall1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*60 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

##bedroom

with open('csv files/tubelight3.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "tubelight", "time": "10", "topic": "1003", "start": "0", "end": "0", "message": "ON",
					  "from": "user_name", "watt": "40", "duty_cycle": "98", "category": "actuator", "ack_val": "null","room":"bed1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])/40 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i=i+1

with open('csv files/fan3.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "fan", "time": "5", "topic": "2003", "start": "0", "end": "0", "message": "2",
				"from": "user_name", "watt": "80", "duty_cycle": "95", "category": "actuator", "ack_val": "null",
				"room": "bed1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*18 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port5.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4005", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "bed1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*70 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port6.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4006", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "bed1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*90 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port7.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4007", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "bed1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*23 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/iron1.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x={ "type" : "iron", "time":"0.5", "topic" : "5001", "start" : "0", "end" : "0", "message" : "1", "from" : "user_name", "watt":"1000","duty_cycle":"80", "category":"actuator", "ack_val": "null","room": "bed1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*1000 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

##KITCHEN
with open('csv files/tubelight4.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "tubelight", "time": "10", "topic": "1004", "start": "0", "end": "0", "message": "ON",
					  "from": "user_name", "watt": "40", "duty_cycle": "98", "category": "actuator", "ack_val": "null","room":"kitchen"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])/40 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i=i+1

with open('csv files/fan4.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "fan", "time": "5", "topic": "2004", "start": "0", "end": "0", "message": "ON",
				"from": "user_name", "watt": "80", "duty_cycle": "95", "category": "actuator", "ack_val": "null",
				"room": "kitchen"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*15 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port8.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4008", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "kitchen"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*29 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/port9.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4009", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "kitchen"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*50 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1


##bathroom
with open('csv files/tubelight5.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type": "tubelight", "time": "10", "topic": "1005", "start": "0", "end": "0", "message": "ON",
					  "from": "user_name", "watt": "40", "duty_cycle": "98", "category": "actuator", "ack_val": "null","room":"bathroom1"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])/40 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i=i+1

with open('csv files/port10.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = {"type" : "port", "time":"6", "topic" : "4010", "start" : "0", "end" : "0", "message" : "ON", "from" : "user_name", "watt":"15","duty_cycle":"100", "category":"actuator", "ack_val": "null","room": "bathroom"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*100 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i = i + 1

with open('csv files/heater1.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = { "type" : "water_heater", "time":"0.5", "topic" : "7001", "start" : "0", "end" : "0", "message" : "0", "from" : "user_name", "watt":"1500","duty_cycle":"90", "category":"actuator", "ack_val": "null","room": "bathroom"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*1500 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i=i+1

with open('csv files/washing_machine.csv','r') as f:
	reader = csv.reader(f)
	for row in reader:
		print(row)
		x = { "type" : "waching_machine", "time":"3", "topic" : "8001", "start" : "0", "end" : "0", "message" : "0", "from" : "user_name", "watt":"500","duty_cycle":"98", "category":"actuator", "ack_val": "null","room": "bathroom"}
		x['start'] = str((float(row[0])*24*3600) + (3600*float(row[1])))
		x['end'] = str(float(row[2])*24*3600 + 3600*float(row[3]))
		x['message'] = str(float(row[4]))
		x['watt'] = str(float(row[4])*400 + 3)
		x['from'] = str(row[5])
		k = mydb.temp.insert_one(x)
		i=i+1

print("Number of records entered = ",i)