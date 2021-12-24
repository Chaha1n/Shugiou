
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
        return int(data_str.split("\r")[0])   
 
def publish(client,topic,message):
    client.publish(topic,json.dumps(message))
    print(json.dumps(message))

      
  
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("サーバーに接続しました")
    else:
        print("Failed to connect, return code %d\n", rc)        



def connect_mqtt(client_user):
    client_id = 'device' + client_user
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client




def get_standard_smell():
    print("基準値を取得しています")
    standard_value=0
    for i in range(10):
        standard_value+=int(Sensor().read())
    standard_value/=10
    return standard_value
        

def main():
   
    print("プレイヤー名を入力")
    username=input()

    print("合言葉を入力")
    topic=input()

    client = connect_mqtt(username)
    client.loop_start()

    sensor = Sensor()


    #時間が10秒かかります
    standard_value=get_standard_smell()

    #試合開始判定処理はここに書くことになるのかな？
    
    #client.subscribe(topic)

    while True:
        smell=sensor.read()
        smell=str(smell-standard_value)
        #基準値から引いた値をpub
        message = {"name" : username,"value" : smell}
        publish(client,topic,message)




if __name__ == '__main__':
    main()