"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import time
import configparser
import json
<<<<<<< HEAD
from pymongo import MongoClient 
from bson.json_util import dumps

=======
from pymongo import MongoClient
from bson.json_util import dumps
>>>>>>> 80a53679f2999ac2e8c2dc25c837306360968d89

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
x = mycol.delete_many({})
print(x.deleted_count, " documents deleted from collection condevs.") 
mongoclient.close()


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
	message_string = msg.payload.decode('utf-8')

	print ("Topic: ", msg.topic + "\nMessage: " + message_string)

	if msg.topic == 'conf' and message_string[0] == '{':
		
		# extract the message from JSON and check type
<<<<<<< HEAD
		parsed_json = parsetoJson(message_string)
		if(parsed_json['type'] == 'mobile'):
			try:
			# fetch from mongo and send everything to mobile
				mongoclient = MongoClient(mongo_host, mongo_port_no)
				print('mongoclient:', mongo_host, mongo_port_no)
				mydb = mongoclient[mongo_database_name]	

				device_topic = parsed_json['topic']	#on this topic, message is published

				print("device topic search results::::",mydb.connected_devices.find({"topic": device_topic}))
				#if mydb.connected_devices.find({"topic": device_topic}) == None:
				#	print('Inserting mobile device for the first time in connected_devices..')
					# inserting the mobile also in connected_devices	
				#	mydb.connected_devices.insert_one(parsed_json)	

				print('database:',mydb)
				for x in mydb.connected_devices.find():
					print("Publishing for mobile initialization...",dumps(x))
					client.publish(device_topic, dumps(x))
			except Exception as ex:
				print('Error connecting to mongodb! {0}'.format(type(ex).__name__))
		mongoclient = MongoClient(mongo_host, mongo_port_no)
		mydb = mongoclient[mongo_database_name]
		mydb.connected_devices.update_one(
        	{"topic":device_topic},
        	{
            	"$set": parsed_json,
        	},
        upsert=True)
=======
		parsed_json = parseJson(message_string)
		mongoclient = MongoClient(mongo_host, mongo_port_no)
		mydb = mongoclient[mongo_database_name]
		#mycol=mydb["condevs"]
		
		if(parsed_json['type'] == 'mobile'):
			#extract collection convs and send all documents one by one and at last donedb
			print("Requested by mobile device")
			print("publishing to mobile")
			for x in mydb.connected_devices.find():
							
				client.publish('mobile',str(x))
				
			client.publish('mobile',done)

		else:
			print("Not a mobile device")
			print("publishing to mobile")
			client.publish('mobile', message_string)
		#print(parsed_json['name'])
		#mongoclient = MongoClient(mongo_host, mongo_port_no)
		#mydb = mongoclient[mongo_database_name]
		mydb.connected_devices.insert_one(parsed_json)
		mongoclient.close()

		#publish to mobile whenever new device enters in system

>>>>>>> 80a53679f2999ac2e8c2dc25c837306360968d89

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
{"company":"samsung", "type":"mobile","modelno":"567890", "uid":"ABC456", "topic":"mobile1"}

"""





