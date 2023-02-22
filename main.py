import sys
import os
import random
import serial.tools.list_ports
import time
from Adafruit_IO import MQTTClient
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('ADAFRUIT_USERNAME')
ADAFRUIT_API = os.getenv('ADAFRUIT_API')

def connected(client):
  print("Connect successfully!")
  client.subscribe('test')

def subscribe(client, userdata, mid, granted_qos):
  print("Subscribe sucessfully!")

def disconnected(client):
  print("Disconnected!")
  sys.exit(1)

def message(client, feed_id, payload):
  print("Received message: ", payload)

def get_port():
  ports = serial.tools.list_ports.comports()
  print(ports)
  number_of_ports = len(ports)
  comm_port = "None"
  for i in range (0 , number_of_ports ) :
    port = ports [ i ]
    strPort = str ( port )
    if " USB Serial Device " in strPort :
      splitPort = strPort . split ( " " )
      comm_port = ( splitPort [0])
  return comm_port

ser = serial.Serial(port=get_port(), baudrate=115200)

mqtt_client = MQTTClient(USERNAME, ADAFRUIT_API)
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message
mqtt_client.on_subscribe = subscribe
mqtt_client.connect()
mqtt_client.loop_background()

while True:
  value = random.randint(0,100)
  print("Update: ", value)
  mqtt_client.publish('test', value)
  time.sleep(5)
