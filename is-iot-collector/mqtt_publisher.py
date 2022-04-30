import utils
import json
from logger import LOG
import paho.mqtt.client as mqttclient

class MQTTPublisher:
    def __init__(self):
        self.__host = utils.get_setting("mqtt/host")
        self.__id = utils.get_setting("id")
        self.__topic = utils.get_setting("mqtt/topics/data")
        self.__registrationTopic = utils.get_setting("mqtt/topics/registration")
        self.__client = mqttclient.Client("collector" + self.__id)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.connect(self.__host)
        self.__client.loop_start()
        #TODO: use authentication

    def connect(self):
        if not self.__client.is_connected():
            self.__client.connect(self.__host)
            
    def register(self):
        try:
            self.connect()
        except Exception as ex:
            LOG.err("MQTT Client failed to connect!")
            return

        register_message = json.dumps({'collectorId' : self.__id})
        try:
            self.__client.publish(self.__registrationTopic, register_message)
            LOG.info("Collector registered succesfully!")
        except Exception as ex:
            LOG.err("MQTT Client failed to publish!")

    def publish(self, message: str):
        try:
            self.connect()
        except Exception as ex:
            LOG.err("MQTT Client failed to connect!")
            return

        try:
            self.__client.publish(self.__topic, message)
        except Exception as ex:
            LOG.err("MQTT Client failed to publish!")

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to connect! Error code = {}".format(rc))
        else:
            LOG.info("MQTT Client connected successfully!")        
            self.register()

    def __on_disconnect(self, client, userdata, rc):
        self.__client.loop_stop()
        if rc != 0:
            LOG.err("MQTT Client failed to disconnect! Error code = {}".format(rc))
        else:
            LOG.info("MQTT Client disconnected successfully!")
