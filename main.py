
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json


ENDPOINT = "agmxgja9ihm7-ats.iot.ap-northeast-1.amazonaws.com"
PATH_TO_CERTIFICATE = "./secret/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "./secret/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./secret/AmazonRootCA1.pem"


RANGE = 5

print("プレイヤー名を入力してね")
username=input()
CLIENT_ID = "Device"+username
print("合言葉を入力してね")
TOPIC=input()



# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')
for i in range (RANGE):
    username = "plmwa"
    nioi = "100"
    message = {"name" : username,"value" : nioi}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print(json.dumps(message))
    t.sleep(0.1)
print('Publish End')
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
