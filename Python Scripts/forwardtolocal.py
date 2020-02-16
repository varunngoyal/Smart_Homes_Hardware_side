"""
Python MQTT Subscription client

*************************************************************
Forwards the traffic from the local network to Cloudmqtt
*************************************************************

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
        print("Connected to ("+raspi_uname+", "+raspi_pass+")")
    else:
        print ("Failing to establish connection.. returned with error code",rc)
    # Once the client has connected to the broker, subscribe to the topic

    client.subscribe("actuator")
    client.subscribe("timer")
    client.subscribe("sensor")
    client.subscribe("conf")

    print("Subscription to", "actuator", "successful!");
    print("Subscription to", "timer", "successful!");
    print("Subscription to", "sensor", "successful!");
    print("Subscription to", "conf", "successful!");


def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function

    message_string = msg.payload.decode('utf-8')
    print("Topic: ", msg.topic + "\nMessage: " + message_string)

    if msg.topic == "actuator":
        client_raspi.publish("actuator", message_string)
    elif msg.topic == "sensor":
        client_raspi.publish("sensor", message_string)
    elif msg.topic == "timer":
        client_raspi.publish("timer", message_string)
    elif msg.topic == "conf":
        client_raspi.publish("conf", message_string)


    print("The message has been published to cloudmqtt!")

    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client_cloudmqtt.on_connect = on_connect
client_cloudmqtt.on_message = on_message



# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using

while True:
    try:
        #print("",end='')
        client_cloudmqtt.connect(mqtt_server, mqtt_port_no)
        client_raspi.connect(local_ip, local_port_no)
        break
    except Exception as e:
        # Stop the internal worker
        #client._mqtt_core._event_consumer.stop()
        print(type(e).__name__)
        print("Failing to establish connection...trying again...")
        time.sleep(1)
        continue


# Once we have told the client to connect, let the client object run itself
client_cloudmqtt.loop_forever()
client_cloudmqtt.disconnect()

