
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
from time import sleep

import serial



ENDPOINT = "agmxgja9ihm7-ats.iot.ap-northeast-1.amazonaws.com"
PATH_TO_CERTIFICATE = "./secret/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "./secret/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./secret/AmazonRootCA1.pem"

during_match = True

class Client:
    def __init__(self,user_name,watchword):
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        client_id = 'device' + user_name

        self.client =  mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=client_id,
            clean_session=False,
            keep_alive_secs=6
        )

    def connect(self):
        print("サーバーに接続中")
        connect_future = self.client.connect()
        connect_future.result()
        print("接続しました")

    def disconnect(self):
        disconnect_future = self.client.disconnect()
        disconnect_future.result()

    def subscribe(self,topic,callback):
        print("合言葉'{}'でプレイします".format(topic))
        sub_future,packet_id = self.client.subscribe(
            topic = topic, 
            qos = mqtt.QoS.AT_LEAST_ONCE, 
            callback = callback
        )
        sub_future.result()

    def publish(self,topic,message):
        self.client.publish(topic=topic, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)

class Sensor:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', 115200)

    def read(self):
        data_str = self.serial.readline().decode()
        return data_str.split("\r")[0]   
    

def on_message(topic,payload,**kwargs):
    global during_match
    # When we recieved message from browser like "finished", finish the match.   
    payload_json = json.loads(payload.decode())
    if('message' in payload_json and payload_json['message'] == "finished"): #temporary False
           during_match = False

def main():
    global during_match
    # Spin up resources
    sensor = Sensor()

    print("プレイヤー名を入力")
    username=input()

    print("合言葉を入力")
    watchword=input()

    client = Client(username,watchword)
    
    # Make the connect
    client.connect()
    #To receive message from browse, we have to subscribe too.
    client.subscribe(watchword,on_message) 
    while during_match:
        sleep(1)
        smell = sensor.read()
        message = {"name" : username,"value" : smell}
        client.publish(watchword,message)

if __name__ == "__main__":
    main()
