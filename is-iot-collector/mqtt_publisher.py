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
            self.__client.loop_start()
            self.__client.publish(self.__registrationTopic, register_message)
            self.__client.loop_stop()
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
            self.__client.loop_start()
            self.__client.publish(self.__topic, message)
            self.__client.loop_stop()
        except Exception as ex:
            LOG.err("MQTT Client failed to publish!")

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to connect! Return code = {}".format(rc))

    def __on_disconnect(self, client, userdata, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to disconnect! Return code = {}".format(rc))
