#!/usr/bin/python
#
#simple app to read string from serial port
#and publish via MQTT
#
#uses the Python MQTT client from the Mosquitto project
#http://mosquitto.org
#
#Matthew Nichols http://mattnics.com
#2019/7/3




import serial,os,json
import xml.etree.ElementTree as ET
import paho.mqtt.publish as publish


serialdev = '/dev/ttyUSB0'
broker = "10.0.3.11"
port = 1883

def cleanup():
    print ("Ending and cleaning up")
    ser.close()
    mqttc.disconnect()

# Connect Serial and bomb out if not connected

try:
    print ("Connecting... "), serialdev
    #connect to serial port
    ser = serial.Serial(serialdev, 57600, timeout=3)
except:
    print ("Failed to connect serial")
    #unable to continue with no serial input
    raise SystemExit

try:
    #read data from serial port
            while True:
                # Read the XML from serial
                line = ser.readline()
                line = line.decode('utf-8')
                #need to handle empty lines and the summary line
                if "watts" in line:
                    # Parse the XML to capture the temperature and the Power COnsuption from my sensor
                    root = ET.fromstring(line)
                    temp = root[3].text
                    power = root[7][0].text
                    print (temp+" "+power)
                    #Update MQTT with values
                    values = {
                        "temp":temp,
                        "power":power
                    }
                    json_output = json.dumps(values)
                    publish.single("home/garage/powermeter", json_output, hostname=broker)


    
# handle list index error (i.e. assume no data received)
except (IndexError):
    print ("No data received within serial timeout period")
    cleanup()
# handle app closure
except (KeyboardInterrupt):
    print ("Interrupt received")
    cleanup()
except (RuntimeError):
    print ("uh-oh! time to die")
    cleanup()
