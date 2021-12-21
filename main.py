
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
from time import sleep


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
        print("connecting...")
        connect_future = self.client.connect()
        connect_future.result()
        print("connected.")

    def disconnect(self):
        print("disconnecting...")
        disconnect_future = self.client.disconnect()
        disconnect_future.result()
        print("disconnected.")

    def subscribe(self,topic,callback):
        print("subscribing to topic '{}'".format(topic))
        sub_future,packet_id = self.client.subscribe(
            topic = topic, 
            qos = mqtt.QoS.AT_LEAST_ONCE, 
            callback = callback
        )
        sub_future.result()
        print("subscribed.")

    def publish(self,topic,message):
        print("publishing message '{}' to topic  '{}'".format(message,topic))
        self.client.publish(topic=topic, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
        print("published.")


class TGS2450:
    def read(self):
        self.heat_once()
        return 100 #temporary value

    # Heat up sensor
    def heat_once(self):
        sleep(0.25) #Just wait for 0.25 sec for now
    
    def heat(self):
        print("Heating up TGS2450.Please wait for a moment...")
        for i in range(40): #10 sec
            self.heat()


def on_message(topic,payload,**kwargs):
    global during_match
    print("Received message from topic '{}': {}".format(topic, payload))
    # When we recieved message from browser like "finished", finish the match.    
    if(False): #temporary False
           during_match = False

def main():
    global during_match
    # Spin up resources
    sensor = TGS2450()
    sensor.heat()

    print("プレイヤー名を入力してね")
    username=input()

    print("合言葉を入力してね")
    watchword=input()

    client = Client(username,watchword)
    
    # Make the connect
    client.connect()
    #To receive message from browse, we have to subscribe too.
    client.subscribe(watchword,on_message) 
    while during_match:
        smell = sensor.read()
        message = {"name" : username,"value" : smell}
        client.publish(watchword,message)

if __name__ == "__main__":
    main()
