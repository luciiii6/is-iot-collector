import utils
import json
import os
import logging
import paho.mqtt.client as mqttclient


class MQTTPublisher:
    def __init__(self):        
        self.__host = os.getenv('MQTT_HOST')
        self.__port = int(utils.get_setting("mqtt/port"))
        self.__qos = int(utils.get_setting("mqtt/qos"))
        self.__auth = utils.get_setting("mqtt/auth")
        self.__id = utils.get_setting("id")
        self.__dataTopic = utils.get_setting("mqtt/topics/data")
        self.__registrationTopic = utils.get_setting("mqtt/topics/registration")
        self.__client = mqttclient.Client("collector" + self.__id)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect

        if self.__auth.lower() == "on":
            self.__client.username_pw_set(os.getenv('MQTT_USERNAME'), os.getenv('MQTT_PASSWORD'))

        self.__client.connect(self.__host, self.__port)
        self.__client.loop_start()

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

mqtt_client = MQTTPublisher()
