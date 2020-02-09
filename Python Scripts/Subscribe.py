"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import time
import configparser
import json


######################################################################################
#------------------ALL THE CONFIGURATIONS---------------------------------------------
######################################################################################
# Read all the credentials from raspy file 
config = configparser.ConfigParser()
config.read('raspy.properties')

# MQTT credentials (Cloudmqtt)
mqtt_username = config.get('mqttCreds', 'mqtt.username')
mqtt_password = config.get('mqttCreds', 'mqtt.password')
mqtt_topic = "led1"
mqtt_server = config.get('mqttCreds', 'mqtt.server')
mqtt_port_no = int(config.get('mqttCreds', 'mqtt.port_no'))

# Rasp Pi credentials
raspi_uname = config.get('raspiCreds', 'raspi.username')
raspi_pass = config.get('raspiCreds', 'raspi.password')

# Local Network credentials
local_ip = config.get('localnetwork', 'local.ip')
local_port_no = int(config.get('localnetwork', 'local.port_no'))

#######################################################################################

client = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(raspi_uname, raspi_pass)

# function() parseJson - returns parsed json
def parseJson(message_string):
	try:
		print(message_string)
		parsed_json = json.loads(message_string)
		return parsed_json
	except Exception as ex:
		print('The error of the type {0} has occured!'.format(type(ex).__name__))

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):	
	# rc is the error code returned when connecting to the broker
	print ("Connected!", str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
	client.subscribe("led1")
	client.subscribe("led2")
	client.subscribe("led1status")	
	client.subscribe("mobile")



	print("Subscription to", "led1", "successful!")

    
def on_message(client, userdata, msg):
	# This function is called everytime the topic is published to.
	# If you want to check each message, and do something depending on
	# the content, the code to do this should be run in this function

	message_string = msg.payload.decode('utf-8')    
	topic = msg.topic
	#client.publish("conf", "dsfds")	

	print()
	#print ("Topic: ", msg.topic + "\nMessage: " + message_string)


	if msg.topic == "led1":
		print('Inside led1')

		# check if payload is containing the field send equals true
		parsed_message = parseJson(message_string)
		if parsed_message["send"] == "true":
			#time.sleep(1)
			#client.publish('conf', '{"company":"samsung", "type":"led","modelno":"123456", "uid":"ABC123", "topic":"led1"}')
			client.publish('ack', 'led1')
			print('published message to led1')


	if msg.topic == 'led2':
		print('Inside led2')
		# check if payload is containing the field send equals true
		print(json.loads(message_string))

		parsed_message = parseJson(message_string)
		if parsed_message["send"] == "true":
			#time.sleep(1)
			#client.publish('conf', '{"company":"samsung", "type":"led","modelno":"123456", "uid":"ABC456", "topic":"led2"}')
			client.publish('ack', 'led2')
			print('published message to led2')
    
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message


# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using

client.connect(local_ip, local_port_no)



#print("Connected")

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
