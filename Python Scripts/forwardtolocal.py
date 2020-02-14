"""
Python MQTT Subscription client

*************************************************************
Forwards the traffic from the cloudmqtt to the local network
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
client2 = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(mqtt_username, mqtt_password)
client2.username_pw_set(raspi_uname, raspi_pass)	#rasp pi


# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected to client",client,"!", str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe("actuator")
    client.subscribe("timer")
    client.subscribe("conf")
    client.subscribe("sensor")

    print("Subscription to", "actuator", "successful!");
    print("Subscription to", "timer", "successful!");
    print("Subscription to", "conf", "successful!");
    print("Subscription to", "sensor", "successful!");



def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    message_string = msg.payload.decode('utf-8')
    print ("Topic: ", msg.topic + "\nMessage: " + message_string)
    
    client2.publish(msg.topic, message_string)
    print("The message has been published to raspberry pi!")
    
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

"""
def on_disconnect(client, userdata, rc):
        print("Unexpected MQTT disconnection. Will auto-reconnect")
        time.sleep(1)
"""

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message
#client.on_disconnect = on_disconnect
# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using


while True:
    try:
        #print("",end='')
        client.connect(mqtt_server, mqtt_port_no)
        client2.connect(local_ip, local_port_no)  # for running on rasp pi

        break
    except Exception as e:
        # Stop the internal worker
        #client._mqtt_core._event_consumer.stop()
        print("Failing to establish connection...trying again...")
        time.sleep(1)
        continue
#client.connect(mqtt_server, mqtt_port_no)
# for running code on other machine than rasp pi
# client2.connect("192.168.0.102", 1883)
#print("Connected")

#print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))

"""
while True:
    #sensor_data = [read_temp(), read_humidity(), read_pressure()]
    client.publish("led1", "1024")
    print("LED ON")
    time.sleep(5)
    client.publish("led1", "0")
    print("LED OFF")
    time.sleep(5)
"""

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()

