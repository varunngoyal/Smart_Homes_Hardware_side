import paho.mqtt.client as mqtt
import time
import threading
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


client1 = mqtt.Client()
client2 = mqtt.Client()
# Set the username and password for the MQTT client
client1.username_pw_set(raspi_uname, raspi_pass)
client2.username_pw_set(raspi_uname, raspi_pass)

mongoclient = MongoClient(mongo_host, mongo_port_no)
mydb = mongoclient[mongo_database_name]
mydb.session.drop()
mydb.actuator.drop()
global ack_message
ack_message = "none"


# function() parseJson - returns parsed json
def parsetoJson(message_string):
	try:
		parsed_json = json.loads(message_string)
		return parsed_json
	except Exception as x:
		print('Error parsing json message: {0}'.format(type(x).__name__))


# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect1(client, userdata, flags, rc):
	# rc is the error code returned when connecting to the broker
	print("Connected!", str(rc))
	# Once the client has connected to the broker, subscribe to the topic
	# client1.subscribe(mqtt_topic)
	client.subscribe("actuator", 2)  # subscriing multiple topics


#	client.subscribe("ack")  			# subscriing multiple topics


print("Subscription to", "actuator", "successful!")


def publish2(a, b):
	print("Trynig to publish on ", a, " message ", b)
	global client2
	client2.publish(a, b)


def on_message1(client, userdata, msg):
	# This function is called everytime the topic is published to.
	# If you want to check each message, and do something depending on
	# the content, the code to do this should be run in this function

	message_string = msg.payload.decode('utf-8')

	print("Topic: ", msg.topic + "\nMessage: " + message_string)



def on_connect2(client, userdata, flags, rc):
	# rc is the error code returned when connecting to the broker
	print("Connected!", str(rc))
	# Once the client has connected to the broker, subscribe to the topic
	# client1.subscribe(mqtt_topic)
	client.subscribe("ack", 2)  # subscriing multiple topics


#	client.subscribe("ack")  			# subscriing multiple topics


def on_message2(client, userdata, msg):
	# This function is called everytime the topic is published to.
	# If you want to check each message, and do something depending on
	# the content, the code to do this should be run in this function
	message_string = msg.payload.decode('utf-8')
	global ack_message
	print("Topic: ", msg.topic + "\nMessage: " + message_string)
	jsonstring=parsetoJson(message_string)
	if msg.topic == 'ack':
		print("ACK topic detected it")
		ack_message = str(jsonstring["ack_message"])
		print(ack_message, " is ack msg from json")
		print('new ')


# The message itself is stored in the msg variable
# and details about who sent it are stored in userdata


# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client1.on_connect = on_connect1
client1.on_message = on_message1

client2.on_connect = on_connect2
client2.on_message = on_message2

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client1.connect(local_ip, local_port_no)
client2.connect(local_ip, local_port_no)

# print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
# client.publish("led1", "0")
"""
while True:
    #sensor_data = [read_temp(), read_humidity(), read_pressure()]
    print("LED ON")
    time.sleep(5)
    client.publish("led1", "0")
    print("LED OFF")
    time.sleep(5)
"""


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


thread2 = threading.Thread(target=trigger2)
thread2.daemon = True
thread2.start()

print("Strarting loop 1")
thread1 = threading.Thread(target=trigger1)
thread1.daemon = True
thread1.start()

#global ack_message
ack_message = 'none'
#global flag_ack
flag_ack = 0

while True:
	# connect to mongo
	mongoclient = MongoClient(mongo_host, mongo_port_no)
	mydb = mongoclient[mongo_database_name]
	connected_devices = mydb["connected_devices"]

	print('mongo client connected to (',mongo_host,',',mongo_port_no,')')
	

	#mydb.temp.delete_many({}) # delete all previous records from temp

	# get topics from mongodb
	topics = []
	print(mydb)
	for x in mydb.connected_devices.find({}):
		print("I'm going in")
		x = dumps(x)
		x = json.loads(x)
		print(x)
		del x['_id']
		topics.append(x['topic'])
		#mydb.temp.insert_one(x)

	print(topics)

	started = time.time()
	print("time started at ", started)
	#x = connected_devices.delete_many({})
	#print(x.deleted_count, " documents deleted.")

	# send request message on every topic
	for topic in topics:
		#check for device ack for 4 seconds
		ack_message = "none"
		client1.publish(str(topic), 'amit')
		topic = str(topic)
		#print('Published request message to devices!')

		while time.time() - started < 4:
			print(" ack_message: ", type(ack_message), ", connected device topic: ", type(topic))
			print(ack_message == topic)
			if ack_message == topic:
				flag_ack = 1
				print("**********strings matched****************")
				break
			time.sleep(1)
		ack_message = "none"

		if(flag_ack==1):
			myquery = {"topic": topic}
			newvalues = {"$set": { "end": time.time()}}
			mydb.connected_devices.update_one(myquery, newvalues)
			print('connected device '+topic+' updated!')

		else:
			topic_log = mydb.connected_devices.find_one({"topic":topic})
			
			mydb.session.insert_one(topic_log)
			mydb.connected_devices.remove({"topic":topic})
			print(str(topic) +' has been disconnected and removed!')

	end_time = time.time()
	wait_time = 10 - (end_time-started)
	if(wait_time > 0):
		time.sleep(wait_time)

#print('published message')
#while True:
#	time.sleep(2)
#	print('2 seconds passed...')
#	client.publish('led1', '{"send": "true"}')
#	print('published to led')



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


#################################################################################################
"""
db.connected_devices.insertOne({"company":"samsung", "type":"led","modelno":"123456", "uid":"ABC123", "topic":"led1"})
db.connected_devices.insertOne({"company":"samsung", "type":"led","modelno":"123456", "uid":"ABC456", "topic":"led2"})

db.connected_devices.insertOne({'company': 'samsung', 'type': 'led', 'time': '5', 'topic': 'led1', 
'start': 1581139241.9628208, 'end': 0.0, 'message': 'ON', 'from': 'mobile', 'last_message': 'ON'})
db.connected_devices.insertOne({'company': 'samsung', 'type': 'led', 'time': '5', 'topic': 'led2',
 'start': 1580752526.4898863, 'end': 0.0, 'message': 'ON', 'from': 'mobile', 'last_message': 'OFF'})
"""

