import board
import adafruit_dht

class AirProperties:
    def __init__(self) -> None:
        self.__dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

    def get_temperature(self):
        try:
            return self.__dhtDevice.temperature
        except RuntimeError as rtex:
            raise rtex
        except Exception as ex:
            self.__dhtDevice.exit()
            self.__dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

    def get_humidity(self):
        try:
            return self.__dhtDevice.humidity
        except RuntimeError as rtex:
            raise rtex
        except Exception as ex:
            self.__dhtDevice.exit()
            self.__dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

