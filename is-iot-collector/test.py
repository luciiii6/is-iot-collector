import mqtt_client
from logger import LOG

client = mqtt_client.MQTTClient()
client.publish("aaaa")

LOG.info("aaaaaaa")

