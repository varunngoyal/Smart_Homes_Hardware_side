"""
publish messsage after particular time interval 

Mepssage needs to contain attributes as
time
topic
on which it gets to publish after delay of time(seconds) 
"""
import paho.mqtt.client as mqtt
import time
import threading
import configparser
import json
from pymongo import MongoClient 
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
#Trigger function for thread implementation and deciding what to do once timer gets executed
def trigger(t1,topic_timed,k):
    timer = time.clock()
    start = time.time()
    print("Inside thread")
    while time.time() - start < float(t1):
        time.sleep(0.5)#sleep(0.5)   
        #print("\n",time.time()) 
    m=str(k)
    client.publish(topic_timed,m)
    print("Message Published to led1")
    # do something else here.


########################################################################################
#Listen to clients who want to configure themself
#global t1
#global client
client = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(raspi_uname, raspi_pass)

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!", str(rc))
	# Once the client has connected to the broker, subscribe to the topic
    #client1.subscribe(mqtt_topic)
    client.subscribe("timer",2)			#subscriing multiple topics
    #client.subscribe("led1",2)
    #client.publish("conf1", "sdfds")
    print("Subscription to", "timer", "successful!"); 
    

    
def on_message(client, userdata, msg):
    print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload.decode('utf-8')))     #topic contains time, message contains time+to be sent on topic+message to be sent to new device is always in jason
    if msg.topic == 'timer':
        msg_in=str(msg.payload.decode('utf-8'))
        y=json.loads(msg_in)
        t1=y['time']
        t2=y['topic']
        #print("time is ",y["time"]," for msg ",str(msg.payload.decode('utf-8')))
        k=y
        thread= threading.Thread(target=trigger,args=(t1,str(t2),y,))
        thread.daemon = True
        thread.start()
        mongoclient = MongoClient(mongo_host, mongo_port_no)
        mydb = mongoclient[mongo_database_name]
        mydb.time.insert_one(k)

    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata



# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message

client.on_connect = on_connect
client.on_message = on_message

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(local_ip, local_port_no)


#print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
#client.publish("led1", "0")


# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()


#################################################################################################






