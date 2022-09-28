import board
import busio
import logging
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADC:
    def __init__(self):
        try:
            self.__i2c = busio.I2C(board.SCL, board.SDA)
            self.__ads = ADS.ADS1015(self.__i2c)
            self.__connected = True
        except:
            logging.critical("I2C Bus not connected!")
            self.__connected = False
            return
        self.__chans = {}

    def register_pin(self, pin):
        self.__chans[pin] = AnalogIn(self.__ads, pin)

    def raw_value_by_pin(self, pin):
        if self.__connected:
            return self.__chans[pin].value
        else:
            return None
