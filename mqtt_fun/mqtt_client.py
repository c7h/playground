import paho.mqtt.client as mqtt
import logging
from time import sleep


level = logging.INFO
BROKER = raw_input("broker: ")
PORT = 1883
TOPICS = raw_input('topics? (separate by bank): ').split(" ")
if BROKER == '': BROKER = "broker.mqttdashboard.com"

logging.basicConfig(format='%(levelname)s:%(message)s', level=level)

def on_connect(client, userdata, flag, result_code):
	logging.info("mqtt connected: [Code %i]" % result_code)
	for topic in TOPICS:
		logging.info("subscribe to topic [%s]..." % topic)
		client.subscribe(topic)

def on_message(client, userdata, message):
	logging.debug("mqtt message received on topic [%s]" % message.topic)
	print "[%s]:%s" % (message.topic ,str(message.payload))



client = mqtt.Client()

#register callbacks
client.on_connect = on_connect
client.on_message = on_message

#connect to broker
client.connect(BROKER, PORT, keepalive=60)

##run receive_loop:
client.loop_forever(timeout=1.0)

#client.loop_start()
#message = "you should close the door to your garden!".split(" ")
# for t in message:
# 	payload = message.pop(0)
# 	for t in TOPICS:
# 		client.publish(t, payload)
# 	sleep(1)
#client.loop_stop()