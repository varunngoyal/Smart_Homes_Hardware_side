"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import time
import configparser
import json
import threading

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

done='{\"value\":\"done\"}'

#######################################################################################

# Initialization routine clear database collections if any

# delete collection connected_devices
mongoclient = MongoClient(mongo_host, mongo_port_no)
mydb = mongoclient[mongo_database_name]
mycol=mydb["connected_devices"]


client1 = mqtt.Client()
client2 = mqtt.Client()
client1.username_pw_set(raspi_uname, raspi_pass)
client2.username_pw_set(raspi_uname, raspi_pass)


def parsetoJson(message_string):
	try:
		parsed_json = json.loads(message_string)
		return parsed_json
	except Exception:
		print('Error parsing json message!')

def on_connect1(client, userdata, flags, rc):
    print ("Connected!", str(rc))
    client.subscribe("conf",2)

    print("Subscription to", "conf", "successful!"); 
    
def on_message1(client, userdata, msg):
	global client2
	mongoclient = MongoClient(mongo_host, mongo_port_no)
	mydb = mongoclient[mongo_database_name]
	mycol = mydb["connected_devices"]

	message_string = msg.payload.decode('utf-8')

	print ("Topic: ", msg.topic + "\nMessage: " + message_string)

	print(message_string[0])
	if msg.topic == 'conf' and message_string[0] == '{':

		parsed_json = parsetoJson(message_string)
		print(parsed_json['type'])
		device_topic = parsed_json['topic']  # on this topic, message is published

		if(parsed_json['type'] == 'mobile'):
			try:
				print('device topic: '+device_topic)
				print("device topic search results::::",mydb.connected_devices.find({"topic": device_topic}))

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
		publish2("mobile",parsed_json)
		print('Data updated!')


def publish2(a,b):
	a=str(a)
	b=str(b)
	print("Trynig to publish on ",a, " message ", b)
	global client2
	client2.publish(a,b)

client1.on_connect = on_connect1
client1.on_message = on_message1

client1.connect(local_ip, local_port_no)
client2.connect(local_ip, local_port_no)

def trigger2():
	print("starting loop 2")
	global client2
	client2.loop_forever()
	client2.disconnect()

def trigger1():
	print("starting loop 1")
	global client1
	client1.loop_forever()
	client1.disconnect()

thread2= threading.Thread(target=trigger2)
thread2.daemon = True
thread2.start()

print("Strarting loop 1")
thread1= threading.Thread(target=trigger1)
thread1.daemon = True
thread1.start()

while 1:
	i=0

#################################################################################################
"""
db.connected_devices.insertOne({"type" : "ldr", "time" : "5", "topic" : "301",
 "start" : 1581139241.9628208,
 "end" : 1581150998.1089, "message" : "ON", "Watt":10,"duty_cycle":10,"ack_val":0})
 db.connected_devices.insertOne({"type" : "temp", "time" : "5", "topic" :"401",
 "start" : 1581139241.9628208,
 "end" : 1581150998.1089, "message" : "ON", "Watt":10,"duty_cycle":10,"ack_val":0})
"""





