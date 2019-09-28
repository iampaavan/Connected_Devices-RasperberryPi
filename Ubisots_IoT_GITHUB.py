'''
Created on April 18, 2019

@author: Paavan Gopala
'''

import sys
sys.path.insert(0, '/home/pi/workspace/iot-device/connected-devices-python/apps')
from labs.module02 import SmtpClientConnector
import time
import requests
import random
from sense_hat import SenseHat
import json

my_device = "raspberrypi"  # My Device label
my_temp_var = "temperature"  # My First variable label
my_humid_var = "humidity"  # My Second variable label
my_press_var = "pressure"  # My Third variable label
my_co_ordinates = "position"  # My Fourth Variable
my_auth_token = "YOUR PERSONAL AUTH TOKEN"  # My Auth TOKEN

conn = SmtpClientConnector.SmtpClientConnector()  # instance for SMTP client

"""Function to create the pay-load to send to cloud and returns the pay-load"""
"""@parameter: temp, humid, press and pos."""


def my_payload(temp, humid, press, pos):
    # Creates three variables for sending data
    instance = SenseHat()  # create a sense-hat instance
    result_temp = instance.get_temperature()  # get temperature readings from sense-hat.
    result_humd = instance.get_humidity()  # get humidity readings from sense-hat.
    result_press = instance.get_pressure()  # get pressure readings from sense-hat.
    
    """Generate Random Co-Ordinates for Country - India"""
    lat = random.randrange(10, 26, 1) + random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(77, 88, 1) + random.randrange(1, 1000, 1) / 1000.0
    
    """Structuring the Pay-load as desired"""
    payload = {temp: result_temp,
               humid: result_humd,
               press: result_press,
               pos:{"value": lat, "context": {"lat": lat, "lng": lng}}}
               
    """Send Email when the below conditions are triggered."""           
    if result_temp >= 35 or result_humd >= 42 or result_press >= 1015:
        
        """Trigger the Email Notification if the above if condition is true."""
        conn.publishMessage('Warning!! Weather conditions not ideal', json.dumps(payload))
        
        """Actuator --> Sense-hat --> Display the message on the LED Screen."""
        instance.show_message('Emergency', text_colour=(0, 255, 0))
        
        print ("Email Triggered.")  # print the message on the user console
               
    return payload


"""HTTP Post Method to send the pay-load to Ubidots Cloud Service"""
"""@parameter: pay-load --> Sensor Data"""

def my_http_post_request(payload):
    
    """Create the headers for the HTTP requests""" 
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, my_device)
    headers = {"X-Auth-Token": my_auth_token, "Content-Type": "application/json"}

    """HTTP Requests made to handle error cases.""" 
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    """Error Case: Processes results and print user friendly info on the console.""" 
    if status >= 400:
        
        print("[ERROR] We are not able to send data after 5 attempts, please check \
            your token credentials and internet connection")
        
        return False

    """Connection Successfully Established: Print the user friendly message on the console"""
    print("[INFO] HTTP Request Successful. Your device is now connected and updated with sensor details.")
    
    return True


"""Driver Code."""

def main():
    
    """Call the payload method and store the object in the variable --> payload."""
    payload = my_payload(
        my_temp_var, my_humid_var, my_press_var, my_co_ordinates)

    """Print the user friendly details on the console for better understanding of the code flow."""
    print("[INFO] Attemping to send data")
    
    """Call the HTTP Post method and pass the @parameter payload to the function"""
    my_http_post_request(payload)
    
    """Display the sensor data (payload) on the screen"""
    print(payload)
    
    """Display the message to the user that the payload is sent successfully to Ubidots."""
    print("[INFO] Payload sent successfully.")
    
    """Display the message to the user that one of the many payload sent successfully to cloud."""
    print("[INFO] Finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
