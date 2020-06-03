import paho.mqtt.client as paho

import time

import serial

import locale

import threading

mqttc = paho.Client()

def job():
    while 1:
        s.write("/getAcc/run\r".encode())
        time.sleep(0.1)

# Settings for connection

host = "192.168.43.151"

topic= "velocity"

port = 1883


# Callbacks

def on_connect(self, mosq, obj, rc):

    print("Connected rc: " + str(rc))


def on_message(mosq, obj, msg):

    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");


def on_subscribe(mosq, obj, mid, granted_qos):

    print("Subscribed OK")


def on_unsubscribe(mosq, obj, mid, granted_qos):

    print("Unsubscribed OK")


# Set callbacks

mqttc.on_message = on_message

mqttc.on_connect = on_connect

mqttc.on_subscribe = on_subscribe

mqttc.on_unsubscribe = on_unsubscribe


# Connect and subscribe

print("Connecting to " + host + "/" + topic)

mqttc.connect(host, port=1883, keepalive=60)

mqttc.subscribe(topic, 0)

serdev = '/dev/ttyUSB0'

s = serial.Serial(serdev, 9600)


s.write("+++".encode())

char = s.read(2)

print("Enter AT mode.")

print(char.decode())


s.write("ATMY 0x00\r\n".encode())

char = s.read(3)

print("Set MY 0x00.")

print(char.decode())


s.write("ATDL 0xFFFF\r\n".encode())

char = s.read(3)

print("Set DL 0xFFFF.")

print(char.decode())


s.write("ATID 0x4041\r\n".encode())

char = s.read(3)

print("Set PAN ID 0x4041.")

print(char.decode())


s.write("ATWR\r\n".encode())

char = s.read(3)

print("Write config.")

print(char.decode())

s.write('ATWR\r\n'.encode())

char = s.read(3)

print('Write config.')

print(char.decode())


s.write('ATCN\r\n'.encode())

char = s.read(3)

print('Exit AT mode.')

print(char.decode())

x=[]

s.write("/getAcc/run\r".encode())
time.sleep(0.5)
s.write("/getAcc/run\r".encode())
time.sleep(0.5)
line=s.read(1)
thread_get = threading.Thread(target = job)
thread_get.start()
number=0
while(1):

    line=s.read(6)

    x=line.decode()

    x=locale.atof(x)

    mqttc.publish(topic, x)

    print(x)

    print(number)

    number=number+1

    mqttc.loop()
    
    time.sleep(0.1)