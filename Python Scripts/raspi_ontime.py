import paho.mqtt.client as mqtt
import time
import configparser
import json
from pymongo import MongoClient 
from bson.json_util import dumps

######################################################################################
#------------------ALL THE CONFIGURATIONS---------------------------------------------
######################################################################################

config = configparser.ConfigParser()
config.read('raspy.properties')

# MQTT credentials
mqtt_username = config.get('mqttCreds', 'mqtt.username')
mqtt_password = config.get('mqttCreds', 'mqtt.password')
mqtt_topic_conf = "conf"
mqtt_server = config.get('mqttCreds', 'mqtt.server')
mqtt_port_no = int(config.get('mqttCreds', 'mqtt.port_no'))

# Rasp Pi credentials
raspi_uname = config.get('raspiCreds', 'raspi.username')
raspi_pass = config.get('raspiCreds', 'raspi.password')

# Local Network credentials
local_ip = config.get('localnetwork', 'local.ip')
local_port_no = int(config.get('localnetwork', 'local.port_no'))

# Database credentials
mongo_database_name = config.get('mongo', 'mongo.database')
mongo_port_no = int(config.get('mongo', 'mongo.port_no'))
mongo_host = config.get('mongo', 'mongo.host')

#######################################################################################

#Listen to clients who want to configure themselves

client = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(raspi_uname, raspi_pass)

mongoclient = MongoClient(mongo_host, mongo_port_no)
mydb = mongoclient[mongo_database_name]

start=time.time()
mydb.raspi_on.insert_one({"start":start,"end":0,"ontime":0})
print("started at ",start)

time.sleep(2)
while 1:
	time.sleep(1)
	print("sleeping")
	x=mydb.connected_devices.find_one({ "start": start })
	myquery = { "start": start }
	end=time.time()
	newvalues = { "$set": {"end": end,"ontime":end-start} }
	mydb.raspi_on.update_one(myquery, newvalues)	


#################################################################################################
"""
db.connected_devices.insertOne({"company":"samsung", "type":"led","modelno":"123456", "uid":"ABC123", "topic":"led1"})
db.connected_devices.insertOne({"company":"samsung", "type":"led","modelno":"123456", "uid":"ABC456", "topic":"led2"})


"""

