'''
Created on April 18, 2019

@author: Paavan Gopala
'''

import sys
sys.path.insert(0, '/home/pi/workspace/iot-device/connected-devices-python/apps')
from labs.module02 import SmtpClientConnector
from sense_hat import SenseHat
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import datetime

print(sys.path)  # print the system path on the console
 
"""Provide a random string to connect to AWSIoT MQTT CLient"""
myMQTTClient = AWSIoTMQTTClient("check123mydevice")

"""Provide your AWS End-point to establish the connection"""
myMQTTClient.configureEndpoint("YOUR-ENDPOINT", 8883)

"""Provide your AWS Credentials such as pem file, certificate for secure connection"""
myMQTTClient.configureCredentials("YOUR AWS PEM FILE", "YOUR PRIVATE PEM KEY",
                                  "YOUR CERTIFICATE PEM")

"""Queue to publish message if the device is offline"""
myMQTTClient.configureOfflinePublishQueueing(-1)

"""Draining Frequency"""
myMQTTClient.configureDrainingFrequency(2)

"""Connection Timeout in seconds"""
myMQTTClient.configureConnectDisconnectTimeout(10)

"""Operation Timeout for MQTT Client in seconds"""
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 seconds

"""Create an instance for SMTP Client connector"""
conn = SmtpClientConnector.SmtpClientConnector()

"""Connect securely""" 
myMQTTClient.connect()

"""Publish the relevant data set"""
myMQTTClient.publish("sensor/info", "connected", 0)
 
"""Infinitely Publish the Sensor Data to the AWS IoT Cloud Service"""
while 1:
    now = datetime.utcnow()  # get the current time in UTC time format
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')  # format my date-time module as per my needs.
    instance = SenseHat()  # Create an instance of SenseHat
    result_temp = instance.get_temperature()  # Get the Temperature from Sensehat
    result_humd = instance.get_humidity()  # Get the Humidity from Sensehat
    result_press = instance.get_pressure()  # Get the Pressure from Sensehat
     
    """Structuring my Payload in the desired format."""
    payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(result_temp) + '","pressure": ' 
    +str(result_press) + ',"humidity": ' + str(result_humd) + '}'
    
    print(payload)  # print the payload data on the user console
    
    """Publish the Topic and the Payload Info to the AWS IoT Cloud Service"""
    myMQTTClient.publish("sensor/data", payload, 0)
    
    """Actuator - Sensehat --> Show the message on the LED Screen"""
    instance.show_message('Low')
    
    print ("No Email Triggered.")  # print the message on the console
    sleep(5)  # wait for 5 seconds
    
    if result_temp >= 39:
        
        """Email Notification sent when the temperature is equal to or greater than 39"""
        conn.publishMessage('Warning!!! Temperature Alert:', payload)
        
        """Actuator - Sensehat --> Display on the LED Screen"""
        instance.show_message('High')
        
        print ("Email Notification Triggered.")  # print the message on the user console
        
        sleep(5)  # wait for 5 seconds
        
    sleep(1)  # Delay of 1 second for the next iteration

