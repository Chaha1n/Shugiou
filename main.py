
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

player_name=""
before_match=True

class Sensor:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', 115200)

    def read(self):
        data_str = self.serial.readline().decode()
        return int(data_str.split("\r")[0])   
 
def publish(client,topic,message):
    client.publish(topic,json.dumps(message))
    print(json.dumps(message))

# メッセージが届いたときの処理

def on_message(client, user_data, msg):
    global player_name
    global before_match 
    
    player_name_parsed_from_MQTT_payload=json.loads(msg.payload)
    print(player_name_parsed_from_MQTT_payload["name"])
    if player_name!=player_name_parsed_from_MQTT_payload["name"]:
        before_match=False

def on_connect(client, user_data, flags, rc):
    if rc == 0:
        print("サーバーに接続しました")
    else:
        print("Failed to connect, return code %d\n", rc)        



def connect_mqtt(client_user):
    client_id = 'device' + client_user
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port)
    return client


def get_standard_smell():
    print("基準値を取得しています")
    standard_value=0
    for i in range(10):
        standard_value+=int(Sensor().read())
    standard_value/=10
    return standard_value

def get_percent_smell(sum_smell):
    #kokoha ataiwokaenagarajikantyousei
    max_smell=4000.00
    
    rate_smell=int((sum_smell/max_smell)*100)
    return str(rate_smell)


def main():
    global before_match
    global player_name
    print("プレイヤー名を入力")
    player_name=input()

    print("合言葉を入力")
    topic=input()

    client = connect_mqtt(player_name)
    client.subscribe(topic)
    client.loop_start()

    sensor = Sensor()


    #時間が10秒かかります
    standard_value=get_standard_smell()

    sum_smell=0.00
    while True:
        smell=sensor.read()
        smell=float(smell-standard_value)+5
        sum_smell+=smell
        print(sum_smell)
        rate_smell=get_percent_smell(sum_smell)
        #試合が始まっていないなら0を返す
        if before_match:
            rate_smell=str(0)
        message = {"name" :player_name,"value" : rate_smell}
        publish(client,topic,message)




if __name__ == '__main__':
    main()