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
    topic_name = 'actuator'
    message = '{"_id" : "1", "type" : "mobile", "time" : "5", "topic" : "101", "start" : "0", "end" : "0", "message" : "1024", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}'
    #message = input("What is your message: ")
    print()
    print("topic:", topic_name, "message:",message)
    print()
    print()	
    client.publish(topic_name, message)
    input()

    topic_name = 'actuator'
    message = '{"_id" : "1", "type" : "mobile", "time" : "5", "topic" : "101", "start" : "0", "end" : "0", "message" : "0", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}'
    client.publish(topic_name, message)
    print("topic:", topic_name, "message:",message)
    input()

    """
    topic_name = 'actuator'
    message = '{"_id" : "1", "type" : "fan", "time" : "5", "topic" : "201", "start" : "0", "end" : "0", "message" : "5", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}'
    client.publish(topic_name, message)
    print("topic:", topic_name, "message:",message)
    input()

    topic_name = 'actuator'
    message = '{"_id" : "1", "type" : "fan", "time" : "5", "topic" : "201", "start" : "0", "end" : "0", "message" : "0", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}'
    client.publish(topic_name, message)
    print("topic:", topic_name, "message:",message)
    input()
    """

    

# Once we have told the client to connect, let the client object run itself
client.loop_forever()
client.disconnect()

"""
    topic_name = 'actuator'
    message = '{"_id" : "1", "type" : "led", "time" : "5", "topic" : "101", "start" : "0", "end" : "0", "message" : "1024", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}'

    topic_name = 'actuator'
    message = '{"_id" : "1", "type" : "led", "time" : "5", "topic" : "101", "start" : "0", "end" : "0", "message" : "0", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}'

    topic_name = 'actuator'
    message = '{"_id" : "1", "type" : "fan", "time" : "5", "topic" : "201", "start" : "0", "end" : "0", "message" : "5", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}'

    topic_name = 'actuator'
    message = '{"_id" : "1", "type" : "fan", "time" : "5", "topic" : "201", "start" : "0", "end" : "0", "message" : "0", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}'

#check device init
	topic_name = "conf"
	message = {"_id" : "1", "type" : "mobile", "time" : "5", "topic" : "mobile1", "start" : "0", "end" : "0", "message" : "ON", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"null", "ack_val": "null"}

#sensor check
	topic_name = "sensor"
	message = {"_id" : "1", "type" : "mobile", "time" : "5", "topic" : "401", "start" : "0", "end" : "0", "message" : "ON", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}

	topic_name = "sensor"
	message = {"_id" : "1", "type" : "mobile", "time" : "5", "topic" : "301", "start" : "0", "end" : "0", "message" : "ON", "from" : "mobile", "Watt":"10","duty_cycle":"10", "category":"sensor", "ack_val": "null"}


"""
