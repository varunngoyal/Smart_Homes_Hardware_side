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
    client.subscribe("actuator")			#subscriing multiple topics
#	client.subscribe("ack")  			# subscriing multiple topics


print("Subscription to", "actuator", "successful!")

def publish2(a,b):
#<<<<<<< HEAD

	print("Trying to publish on ",a, " message ", b)
#=======
	a=str(a)
	b=str(b)
	print("Trynig to publish on ",a, " message ", b)
#>>>>>>> 59a624dbfd2aabbb0203e373ee5affdb259d399c
	global client2
	client2.publish(a, b)
	#print('Message published with status '+client2.publish(a,b))

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

	if msg.topic == 'actuator':
		# 1a it forwards the message to respective actuator
		print('Doing 1')
		json_message = parsetoJson(message_string)
		actuator_topic = json_message['topic']
		actuator_message = json_message['message']
		publish2(actuator_topic, actuator_message)

	# 1b if success/ack comes from device forward the message to all mobile devices
			# just check if connected
		started=time.time()
		print("time started at ",started)
		while time.time()-started < 4 :
#<<<<<<< HEAD
			print(" ack_message ",type(ack_message), "actuator topic ", type(actuator_topic) )
#=======
			#print(" ack_message ",type(ack_message), "actuator topic ", type(actuator_topic) )
#>>>>>>> 59a624dbfd2aabbb0203e373ee5affdb259d399c
			if ack_message==actuator_topic:
				flag_ack=1
				#print("strings matched")
				break


		ack_message="none"


# 2 take last message out of connected_devices and save on session collection
		if flag_ack==1:
#<<<<<<< HEAD
			flag_ack=0
#=======
			print("strings matched")
#>>>>>>> 59a624dbfd2aabbb0203e373ee5affdb259d399c
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

			#publish to all mobile devices about activity
			publish2("mobile",json_message)
			#'{"topic":"led1", "message":"ON", "from"="mobile1"}'
			# logging the message as it is 
			# 4 it inserts log message to actuator
			print('Doing 3')
			mydb.actuator.insert_one(json_message)
			
		else :
			print()
			print("Unable to receive ack from device")

			#change ack_val to -1 and semd
			json_message['ack_val']="-1"
			publish2("mobile",json_message)

			print()

def on_connect2(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!", str(rc))
	# Once the client has connected to the broker, subscribe to the topic
    #client1.subscribe(mqtt_topic)
    client.subscribe("ack",0)			#subscriing multiple topics
#	client.subscribe("ack")  			# subscriing multiple topics


def on_message2(client, userdata, msg):
	# This function is called everytime the topic is published to.
	# If you want to check each message, and do something depending on
	# the content, the code to do this should be run in this function
	message_string = msg.payload.decode('utf-8')
	message_topic = msg.topic.decode('utf-8')
	global ack_message
#<<<<<<< HEAD
	print("Topic: ", message_topic + "\nMessage: " + message_string)
	jsonstring=parsetoJson(message_string)
	if message_topic == 'ack':
		print("ACK topic detected it")
#=======
	#print("Topic: ", msg.topic + "\nMessage: " + message_string)
	jsonstring=parsetoJson(message_string)
	if msg.topic == 'ack':
		#print("ACK topic detected it")
#>>>>>>> 59a624dbfd2aabbb0203e373ee5affdb259d399c
		ack_message = str(jsonstring["ack_message"])
		#print(ack_message, " is ack msg from json")
		#print('new ')

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
	j=0


#################################################################################################
"""
db.connected_devices.insertOne({'type': 'led', 'time': '5', 'topic': '101', 
'start': 1581139241.9628208, 'end': 0.0, 'message': 'ON', 'from': 'mobile', 'last_message': 'ON'})

actuator message: 
{ "type" : "led", "time" : "5", "topic" : 101, "start" : "0", "end" : "0", "message" : "1023", "from" : "mobile", "Watt":10,"duty_cycle":10, "category" :"actuator", "ack_val": "null"}

{ "type" : "fan", "time" : "5", "topic" : "201", "start" : "0", "end" : "0", "message" : "5", "from" : "mobile", "Watt":10,"duty_cycle":10, "category" :"actuator", "ack_val": "null"}

{ "_id" : ObjectId("5e3e72a8831e7bd58506028e"), "type" : "led", "time" : "5", "topic" : 101, "start" : ”0”, "end" : “0”, "message" : "ON", "from" : "mobile", "Watt":10,"duty_cycle":10, "category":"sensor", "ack_val": "null"}


"""

