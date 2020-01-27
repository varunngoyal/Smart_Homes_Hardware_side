"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import time
import configparser


######################################################################################
#------------------ALL THE CONFIGURATIONS---------------------------------------------
######################################################################################
# Read all the credentials from raspy file 
config = configparser.ConfigParser()
config.read('raspy.properties')

# MQTT credentials
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

# Initialize clients for CLOUDMQTT and Raspberry Pi
client_raspi = mqtt.Client()
client_cloudmqtt = mqtt.Client()
# Set the username and password for the MQTT client
client_cloudmqtt.username_pw_set(mqtt_username, mqtt_password)

client_raspi.username_pw_set(raspi_uname, raspi_pass)	#rasp pi


# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    if rc == 0:
        print ("Connected!", str(rc))
    else:
        print ("Failing to establish connection.. returned with error code",rc)
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)
    print("Subscription to", mqtt_topic, "successful!"); 
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    
    print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    
    client_cloudmqtt.publish(msg.topic, msg.payload)
    print("The message has been published to cloudmqtt!")
    
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client_raspi.on_connect = on_connect
client_raspi.on_message = on_message



# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using

client_cloudmqtt.connect(mqtt_server, mqtt_port_no)
while True:
    try:
        #print("",end='')
        client_raspi.connect(local_ip, local_port_no)
        break
    except Exception as e:
        # Stop the internal worker
        #client._mqtt_core._event_consumer.stop()
        print("Failing to establish connection...trying again...")
        time.sleep(1)
        continue


# Once we have told the client to connect, let the client object run itself
client_raspi.loop_forever()
client_raspi.disconnect()

