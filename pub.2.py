# -*- coding: utf-8 -*-
import json
import time
import paho.mqtt.client as mqtt  # ライブラリのimport
broker = 'driver.cloudmqtt.com'
port = 18685
username = 'fauyjmuy'
password = 'xqOIXxqOpCi4'


# broker接続時
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))             # 接続結果表示

mqttc = mqtt.Client()    #clientオブジェクト作成
mqttc.on_connect = on_connect  # 接続時に実行するコールバック関数設定
mqttc.username_pw_set(username, password)
mqttc.connect(broker,port, 60)  # MQTT broker接続

mqttc.loop_start() # 処理開始
message = {"name" : "aa","value" : 200}
while 1:
    mqttc.publish("2222", json.dumps(message))  # topic名="Topic1"に "test1"というメッセージを送信
    time.sleep(1)
    print("push")