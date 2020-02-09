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


# function() parseJson - returns parsed json
def parsetoJson(message_string):
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
    #client1.subscribe(mqtt_topic)
	client.subscribe("conf")			#subscriing multiple topics

	print("Subscription to", "conf", "successful!")
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
	message_string = msg.payload.decode('utf-8')

	print ("Topic: ", msg.topic + "\nMessage: " + message_string)
	if msg.topic == 'conf':
		parsed_msg = parsetoJson(message_string)

		mongoclient = MongoClient(mongo_host, mongo_port_no)
		mydb = mongoclient[mongo_database_name]
		mydb.connected_devices.insert_one(parsed_msg)


    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata


# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(local_ip, local_port_no)

while True:

	# connect to mongo
	mongoclient = MongoClient(mongo_host, mongo_port_no)
	mydb = mongoclient[mongo_database_name]
	connected_devices = mydb["connected_devices"]

	print('mongo client connected to (',mongo_host,',',mongo_port_no,')')
	

	#mydb.temp.delete_many({}) # delete all previous records from temp

	# get topics from mongodb
	topics = []
	for x in mydb.connected_devices.find():
		x = dumps(x)
		x = json.loads(x)
		print(x)
		del x['_id']
		topics.append(x['topic'])
		#mydb.temp.insert_one(x)
		print(x, "inserted into temp successfully!")

	print(topics)

	#x = connected_devices.delete_many({})
	#print(x.deleted_count, " documents deleted.")

	# send request message on every topic
	for topic in topics:
		time.sleep(1)
		client.publish(topic, '{"send":"true"}')
		print("Published check status message to "+topic)
	time.sleep(30)
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
client.loop_forever()
client.disconnect()

#################################################################################################
"""
db.connected_devices.insertOne({"company":"samsung", "type":"led","modelno":"123456", "uid":"ABC123", "topic":"led1"})
db.connected_devices.insertOne({"company":"samsung", "type":"led","modelno":"123456", "uid":"ABC456", "topic":"led2"})


"""

