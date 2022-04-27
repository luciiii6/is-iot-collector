import board
import adafruit_dht
import time

class AirProperties:
    def __init__(self) -> None:
        self.__dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

    def get_temperature(self):
        fail_counter = 15
        while fail_counter != 0:
            try:
                temp = self.__dhtDevice.temperature
                if temp != None:
                    return temp

            except Exception as e:
                self.__dhtDevice.exit()
                self.__dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
            fail_counter -= 1
            time.sleep(1)

        return None

    def get_humidity(self):
        fail_counter = 15
        while fail_counter != 0:
            try:
                hum = self.__dhtDevice.humidity
                if hum != None:
                    return hum

            except Exception as e:
                self.__dhtDevice.exit()
                self.__dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
            fail_counter -= 1
            time.sleep(1)

        return None
