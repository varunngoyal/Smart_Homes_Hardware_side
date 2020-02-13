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


while True:
    client.connect(local_ip, local_port_no)
    #sensor_data = [read_temp(), read_humidity(), read_pressure()]
    """
    client.publish("led1", "1024")
    print("LED ON")
    time.sleep(5)
    client.publish("led1", "0")
    print("LED OFF")
    time.sleep(5)
    """
    #topic_name = input("Enter the topic name: ") 
    topic_name = 'led1'
    message = '{"send":"true"}'
    #message = input("What is your message: ")
    print()
    print("topic:", topic_name, "message:",message)
    print()
    print()	
    client.publish(topic_name, message)
    input()
    

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()

"""
    topic_name = 'actuator'
    message = '{"devicename":"Redmi-note-4", "topic":"led1", "type":"led", "company":"Redmi", "uid":"QWE123", "message":"ON","start":"0","end":"0"}'



"""
