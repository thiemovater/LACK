#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this script is used to publish the temperatur of a 1wire sensor DS18B20 and the cpu temperatur of the raspi via mqtt
# the raspi is built into a LACK shelf from IKEA ;-)
# created by Thiemo Vater

import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays
import glob # is needed for global sys parameter

# client, user and device details
broker     = "192.168.1.2" # IP or URL of the mqtt broker
clientID    = "LACK"
device_name = "LACK Python MQTT device"
username    = "mqttuser"
password    = "mqttpassword"

# Reading of temp from DS18B20 device
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-*')[0]
device_file = device_folder + '/w1_slave'

# Reading DS18B20 temperatur
def read_temp():
    valid = False
    temp = 0
    with open(device_file, 'r') as f:
        for line in f:
            if line.strip()[-3:] == 'YES':
                valid = True
            temp_pos = line.find(' t=')
            if temp_pos != -1:
                temp = float(line[temp_pos + 3:]) / 1000.0
#                print("DS18B20 temp read")

    if valid:
        return temp
    else:
        return None

# Reading of cpu temperatur
def cpu_temp():
    valid = False
    cputemp = 0
    with open(r"/sys/class/thermal/thermal_zone0/temp") as File:
        cputemp = float(File.readline()) / 1000.0
        valid = True
#        print("CPU temp read")

    if valid:
        return cputemp
    else:
        return None


# display all incoming messages
def incoming_message (client, userdata, message):
    print("Received operation " + str(message.payload))

#topic = str(message.topic)
#message = str(message.payload.decode("utf-8"))
#print(topic + message)

client = mqtt.Client(clientID) # Create a MQTT client object
client.username_pw_set(username,password) # Use credentials for broker login
client.connect(broker) # Connect to the test MQTT broker
client.subscribe("LACK/LIGHT") # Subscribe to the topic AC_unit
client.on_message = incoming_message # Attach the messageFunction to subscription
client.loop_start() # Start the MQTT client


# Main program loop
while(1):
    try:
        temp = read_temp()
        cputemp = cpu_temp()
        client.publish("LACK/DS18B20", temp) # Publish the temperature measurements to broker
#        print("DS18B20 temp send")
        client.publish("LACK/CPUTEMP", cputemp) # Publish the temperature measurements to broker
#        print("CPU temp send")


        time.sleep(60) # Sleep for a minute
    except Exception as e:
        print ("Oops!", e.__class__, "occurred.")


