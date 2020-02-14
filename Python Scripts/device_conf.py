"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import time
import configparser
import json
#<<<<<<< HEAD
from pymongo import MongoClient 
from bson.json_util import dumps

#=======
from pymongo import MongoClient
from bson.json_util import dumps
#>>>>>> 80a53679f2999ac2e8c2dc25c837306360968d89

 #from array import *

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

done='{\"value\":\"done\"}'

#######################################################################################

# Initialization routine clear database collections if any

# delete collection connected_devices
mongoclient = MongoClient(mongo_host, mongo_port_no)
mydb = mongoclient[mongo_database_name]
mycol=mydb["connected_devices"]

"""
x = mycol.delete_many({})
print(x.deleted_count, " documents deleted from collection condevs.") 
mongoclient.close()
"""

########################################################################################
#Listen to clients who want to configure themselves

client = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(raspi_uname, raspi_pass)

# function() parseJson - returns parsed json
def parsetoJson(message_string):
	try:
		parsed_json = json.loads(message_string)
		return parsed_json
	except Exception:
		print('Error parsing json message!')



# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!", str(rc))
	# Once the client has connected to the broker, subscribe to the topic
    #client1.subscribe(mqtt_topic)
    client.subscribe("conf",2)			#subscriing multiple topics

    print("Subscription to", "conf", "successful!"); 
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
	mongoclient = MongoClient(mongo_host, mongo_port_no)
	mydb = mongoclient[mongo_database_name]
	mycol = mydb["connected_devices"]

	message_string = msg.payload.decode('utf-8')

	print ("Topic: ", msg.topic + "\nMessage: " + message_string)

	print(message_string[0])
	if msg.topic == 'conf' and message_string[0] == '{':
		
		# extract the message from JSON and check type
#<<<<<<< HEAD
		parsed_json = parsetoJson(message_string)
		print(parsed_json['type'])
		device_topic = parsed_json['topic']  # on this topic, message is published

		if(parsed_json['type'] == 'mobile'):
			try:
			# fetch from mongo and send everything to mobile


				print('device topic: '+device_topic)
				print("device topic search results::::",mydb.connected_devices.find({"topic": device_topic}))
				#if mydb.connected_devices.find({"topic": device_topic}) == None:
				#	print('Inserting mobile device for the first time in connected_devices..')
					# inserting the mobile also in connected_devices	
				#	mydb.connected_devices.insert_one(parsed_json)	

				print('database:',mydb)
				for x in mydb.connected_devices.find():
					x = json.loads(dumps(x))
					x['_id'] = "null"
					print("Publishing for mobile initialization...",dumps(x))
					client.publish("mobile", dumps(x))


			except Exception as ex:
				print('Error connecting to mongodb! {0}'.format(type(ex).__name__))

		mongo_host1 = '127.0.0.1'
		mongo_port_no1 = 27017
		mongo_database_name1 = 'mqtt_raspi'
		mongoclient1 = MongoClient(mongo_host1, mongo_port_no1)
		mydb1 = mongoclient1[mongo_database_name1]
		print('outside if '+mongo_host1+''+str(mongo_port_no1))

		parsed_json['start'] = time.time()
		#print('host: '+mongo_host1+', mongoport: '+mongo_port_no1)
		mydb1.connected_devices.update_one(
        	{"topic":device_topic},
        	{
            	"$set": parsed_json,
        	},
        upsert=True)
		print('Data updated!')

#=======

		#publish to mobile whenever new device enters in system

#>>>>>>> 80a53679f2999ac2e8c2dc25c837306360968d89

    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata


# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(local_ip, local_port_no)

#print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
#client.publish("led1", "0")
"""
while True:
    #sensor_data = [read_temp(), read_humidity(), read_pressure()]
    print("LED ON")
    time.sleep(5)
    client.publish("led1", "0")
    print("LED OFF")
    time.sleep(5)
"""

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()

#################################################################################################
"""
db.connected_devices.insertOne({"type" : "led", "time" : "5", "topic" : 101,
 "start" : 1581139241.9628208,
 "end" : 1581150998.1089, "message" : "ON", "Watt":10,"duty_cycle":10})
 db.connected_devices.insertOne({"type" : "led", "time" : "5", "topic" : 102,
 "start" : 1581139241.9628208,
 "end" : 1581150998.1089, "message" : "ON", "Watt":10,"duty_cycle":10})
"""





