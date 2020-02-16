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
# Set the username and password for the MQTT client
client.username_pw_set(raspi_uname, raspi_pass)


# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(local_ip, local_port_no)

while True:
    #sensor_data = [read_temp(), read_humidity(), read_pressure()]
    """
    client.publish("led1", "1024")
    print("LED ON")
    time.sleep(5)
    client.publish("led1", "0")
    print("LED OFF")
    time.sleep(5)
"""    
    topic_name = 'sensor'
    message = '{"company":"samsung","type":"ldr","time":"5","topic":"301","message":"1000","from":"mobile","ack_val":"0","category":"sensor"}'
    #message = '{"company":"samsung","type":"led","time":"5","topic":"led1","start":"0","end":"0","message"="ON","from":"mobile"}'

    print("topic:", topic_name, "message:",message)
    client.publish(topic_name, message)
    input()
    topic_name = 'sensor'
    message = '{"company":"samsung","type":"temp","time":"5","topic":"401","message":"5","from":"mobile","ack_val":"0","category":"sensor"}'
    print("topic:", topic_name, "message:",message)
    client.publish(topic_name, message)
    input()

    

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()
