import utils
from logger import LOG
import paho.mqtt.client as mqttclient

_error = False

class MQTTClient:
    def __init__(self):
        self.__host = utils.getSetting("host")
        self.__name = utils.getSetting("name")
        self.__topic = utils.getSetting("topic")
        self.__client = mqttclient.Client(self.__name)
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        #TODO: use authentication

    def publish(self, message: str):
        _error == False
        try:
            self.__client.connect(self.__host)
            if _error:
                return False

            self.__client.loop_start()

            ret = self.__client.publish(self.__topic, message)
            if ret.rc != 0:
                return False

            self.__client.loop_stop()

            self.__client.disconnect()
            if _error:
                return False
        except Exception as ex:
            LOG.err("MQTT Client failed to publish!")
            return False

    def __on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to connect!")
            error = True
        else:
            error = False

    def __on_disconnect(self, client, userdata, rc):
        if rc != 0:
            LOG.err("MQTT Client failed to disconnect!")
            error = True
        else:
            error = False
