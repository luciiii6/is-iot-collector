import json
import os
import logging
import paho.mqtt.client as mqttclient
from is_iot_collector.settings import Settings

class MQTTClient:
    def __init__(self, settings: Settings):
        self.__settings = settings      
        self.__host = os.getenv('MQTT_HOST')
        self.__port = self.__settings.get("mqtt/port")
        self.__qos = self.__settings.get("mqtt/qos")
        self.__auth = self.__settings.get("mqtt/auth")
        self.__id = self.__settings.get("id")
        self.__client = mqttclient.Client("collector" + self.__id)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message

        if self.__auth.lower() == "on":
            self.__client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))

        self.__client.connect(self.__host, self.__port)
        self.subscribe(self.__registration_topic())
        self.__client.loop_start()

    def connect(self):
        if not self.__client.is_connected():
            self.__client.connect(self.__host, self.__port)

    def publish(self, message: str):
        try:
            self.connect()
        except Exception as ex:
            logging.error("MQTT Client failed to connect!")
            return

        try:
            self.__client.publish(self.__dataTopic, message, self.__qos)
        except Exception as ex:
            logging.error("MQTT Client failed to publish!")

    def send_errors(self, message: str):
        try:
            self.connect()
        except Exception as ex:
            logging.error("MQTT Client failed to connect!")
            return

        try:
            self.__client.publish(self.__errorTopic, message, self.__qos)
        except Exception as ex:
            logging.error("MQTT Client failed to publish!")

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            logging.error("MQTT Client failed to connect! Error code = {}".format(rc))
        else:
            logging.info("MQTT Client connected successfully!")        

    def __on_disconnect(self, client, userdata, rc):
        self.__client.loop_stop()
        if rc != 0:
            logging.error("MQTT Client failed to disconnect! Error code = {}".format(rc))
        else:
            logging.info("MQTT Client disconnected successfully!")

    def __on_message(self, client, userdata, message):
        if message.topic == self.__registration_topic():
            payload = json.loads(str(message.payload.decode("utf-8")))
            self.__settings.set('sinkId', payload['sinkId'])
            self.__dataTopic = '/' + self.__settings.get('sinkId') + self.__settings.get("mqtt/topics/data")
            self.__errorTopic = '/' + self.__settings.get('sinkId') + self.__settings.get('mqtt/topics/errors')
            logging.info(self.__errorTopic)
            logging.info(f"The sink id was received: {self.__settings.get('sinkId')} and topics were initialized")

    def subscribe(self, topic: str):
        self.__client.subscribe(topic, self.__qos)

    def __registration_topic(self):
        return f"/{self.__id}{self.__settings.get('mqtt/topics/registration')}"
