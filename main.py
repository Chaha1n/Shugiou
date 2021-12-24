# python 3.6

import time
import json
import os

from paho.mqtt import client as mqtt_client

import serial

from dotenv import load_dotenv
load_dotenv()

broker = os.environ['broker']
port = int(os.environ['port'])
username = os.environ['username']
password = os.environ['password']
client_id=""

class Sensor:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', 115200)

    def read(self):
        data_str = self.serial.readline().decode()
        return data_str.split("\r")[0]   
 

def connect_mqtt():
    global client_id

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("サーバーに接続しました")

        else:
            print("Failed to connect, return code %d\n", rc)
    
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,topic,message):
    client.publish(topic,json.dumps(message))
    print(json.dumps(message))
        

def main():
    global client_id
   
    print("プレイヤー名を入力")
    username=input()

    client_id = username

    print("合言葉を入力")
    topic=input()

    client = connect_mqtt()
    client.loop_start()

    sensor = Sensor()
    
    #基準値をきめる
    print("基準値を取得しています")
    standard_smell=0
    for i in range(10):
        standard_smell+=int(sensor.read())
    standard_smell/=10

    #試合開始判定処理はここに書くことになるのかな？


    while True:
        smell=int(sensor.read())
        smell=str(smell-standard_smell)
        #基準値から引いた値をpub
        message = {"name" : username,"value" : smell}
        publish(client,topic,message)




if __name__ == '__main__':
    main()