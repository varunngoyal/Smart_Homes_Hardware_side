import paho.mqtt.client as mqtt
import time
import threading
import configparser
import json
from pymongo import MongoClient 
from bson.json_util import dumps


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
ack_message="none"


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
    print ("Connected!", str(rc))
	# Once the client has connected to the broker, subscribe to the topic
    #client1.subscribe(mqtt_topic)
    client.subscribe("actuator",2)			#subscriing multiple topics
#	client.subscribe("ack")  			# subscriing multiple topics


print("Subscription to", "actuator", "successful!")

def publish1(a,b):
	print("Trynig to publish on ",a, " message ", b)
	global client2
	client2.publish(a,b)

def on_message1(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
	global ack_message
	ack_message='none'
	global flag_ack
	flag_ack=0


	message_string = msg.payload.decode('utf-8')

	print ("Topic: ", msg.topic + "\nMessage: " + message_string)

	if msg.topic == 'sensor':
		# 1a it forwards the message to respective actuator
		print('Doing 1')
		json_message = parsetoJson(message_string)
		actuator_topic = json_message['topic']
		actuator_message = json_message['message']
		publish1(actuator_topic, actuator_message)


	# 1b if success/ack comes from device forward the message to all mobile devices
			# just check if connected
		started=time.time()
		print("time started at ",started)
		while time.time()-started < 4 :
			print(" ack_message ",ack_message, "actuator topic ", actuator_topic )
			if ack_message==actuator_topic:
				flag_ack=1
				print("strings matched")
				break
			time.sleep(1)
		ack_message="none"


# 2 take last message out of connected_devices and save on session collection
		if flag_ack==1:
			x=mydb.connected_devices.find_one({ "topic": actuator_topic })
			print('topic',actuator_topic,"found in the connected devices")
			print(x)
			print(x!=None)
			if x!=None:
				y = parsetoJson(dumps(x))
				print("parsed x : ",y)
				# append current time and end time
				y['_id']="A"
				del y['_id']
				y['end'] = time.time()
				#y['message']="hello"
				#print('x to be inserted: ',x)
				k=mydb.session.insert_one(y)	##dont know why it was inserting record twice
				print('Printing k',k)
			else:
				print("Record for device not found")

			# 3 it updates the connected_devices with last message
			print('Doing 2')
			myquery = { "topic": actuator_topic }
			newvalues = { "$set": {"last_message":actuator_message, "start": time.time()} }
			mydb.connected_devices.update_one(myquery, newvalues)
			#'{"topic":"led1", "message":"ON", "from"="mobile1"}'
			# logging the message as it is 
			# 4 it inserts log message to actuator
			print('Doing 3')
			mydb.actuator.insert_one(json_message)
			
		else :
			print("Unable to receive ack from device")


def on_connect2(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!", str(rc))
	# Once the client has connected to the broker, subscribe to the topic
    #client1.subscribe(mqtt_topic)
    client.subscribe("ack",2)			#subscriing multiple topics
#	client.subscribe("ack")  			# subscriing multiple topics


def on_message2(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
	global ack_message
	global flag_ack
	flag_ack=0

	message_string = msg.payload.decode('utf-8')

	print ("Topic: ", msg.topic + "\nMessage: " + message_string)
	if msg.topic == 'ack':
		print("ACK topic detected it")
		ack_message=message_string



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

# Once we have told the client to csonnect, let the client object run itself
while 1:
	i=0


#################################################################################################
"""
{"company":"samsung", "type":"mobile","modelno":"567890", "uid":"ABC456", "topic":"mobile1"}
{ "type" : "ldr", "time" : "5", "topic" : "301", "start" : "0", "end" : "0", "message" : "null", "from" : "mobile", "Watt":10,"duty_cycle":10, "category" :"actuator", "ack_val": "null"}

"""

