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
        self._client.on_message = self.__on_message

        if self.__auth.lower() == "on":
            self.__client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))

        self.__client.connect(self.__host, self.__port)
        self.__client.loop_start()
        self.subscribe(self.__registration_topic())

    def connect(self):
        if not self.__client.is_connected():
            self.__client.connect(self.__host, self.__port)
            
    def register(self):
        try:
            self.connect()
        except Exception as ex:
            logging.error("MQTT Client failed to connect!")
            return

        register_message = json.dumps({'collectorId' : self.__id})
        try:
            self.__client.publish(self.__registrationTopic, register_message, self.__qos)
            logging.info("Collector registered succesfully!")
        except Exception as ex:
            logging.error("MQTT Client failed to publish!")

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

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            logging.error("MQTT Client failed to connect! Error code = {}".format(rc))
        else:
            logging.info("MQTT Client connected successfully!")        
            self.register()

    def __on_disconnect(self, client, userdata, rc):
        self.__client.loop_stop()
        if rc != 0:
            logging.error("MQTT Client failed to disconnect! Error code = {}".format(rc))
        else:
            logging.info("MQTT Client disconnected successfully!")

    def __on_message(self, client, userdata, message):
        if message.topic == f'/{self.__id}/registration/':
            payload = json.loads(str(message.payload.decode("utf-8")))
            self.__settings.set('sinkId', payload['sinkId'])
            self.__dataTopic = '/' + self.__settings.get('sinkId') + self.__settings.get("mqtt/topics/data")
            self.__registrationTopic = '/' + self.__settings.get('sinkId') + self.__settings.get("mqtt/topics/registration")

            logging.info(f"The sink id was received: {self.__settings.get('sinkId')} and topics were initialized")

    def subscribe(self, topic: str):
        self.__client.subscribe(topic, self._qos)

    def __registration_topic(self):
        return f"/{self.__id}/registration"