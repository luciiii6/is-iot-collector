import utils
from logger import LOG
import paho.mqtt.client as mqttclient

class MQTTPublisher:
    def __init__(self):
        self.__host = utils.getSetting("host")
        self.__name = utils.getSetting("name")
        self.__topic = utils.getSetting("topic") + self.__name + "/"
        self.__registrationTopic = utils.getSetting("registrationTopic")
        self.__client = mqttclient.Client(self.__name)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        #TODO: use authentication

    def register(self):
        try:
            self.__client.connect(self.__host)
            self.__client.loop_start()
            self.__client.publish(self.__registrationTopic, self.__topic)
            self.__client.loop_stop()
            self.__client.disconnect()
            LOG.info("Collector registered succesfully!")
        except Exception as ex:
            LOG.err("MQTT Client failed to publish!")

    def publish(self, message: str):
        try:
            self.__client.connect(self.__host)
            self.__client.loop_start()
            self.__client.publish(self.__topic, message)
            self.__client.loop_stop()
            self.__client.disconnect()
        except Exception as ex:
            LOG.err("MQTT Client failed to publish!")

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to connect! Return code = {}".format(rc))

    def __on_disconnect(self, client, userdata, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to disconnect! Return code = {}".format(rc))
