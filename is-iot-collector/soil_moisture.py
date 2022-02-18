from unittest import result
import board
import busio
import utils
import adafruit_ads1x15.ads1015 as ADS
from logger import LOG
from adafruit_ads1x15.analog_in import AnalogIn

class SoilMoisture:
    def __init__(self):
        try:
            self.__i2c = busio.I2C(board.SCL, board.SDA)
            self.__ads = ADS.ADS1015(self.__i2c)
            self.__connected = True
        except:
            LOG.critical("I2C Bus not connected!")
            self.__connected = False
            return
        
        pins = self.__parse_pins()
        if len(pins) == 0:
            LOG.critical("Invalid pin configuration!")

        self.__chans = {}
        for i in pins:
            try:
                self.__chans[i] = AnalogIn(self.__ads, i)
            except ValueError as e:
                LOG.critical(e)

        self.low_limit = int(utils.get_setting('soilMoisture/lowLimit'))
        self.high_limit = int(utils.get_setting('soilMoisture/highLimit'))

    def get_one_moisture_percent(self, pin: int):
        if not self.__connected:
            LOG.critical("I2C Bus not connected!")
            return None

        if len(self.__chans) == 0:
            LOG.critical("No channels available!")
            return None

        if pin not in self.__chans.keys():
            LOG.critical("No channel found on pin: {}".format(pin))
            return None

        return self.__calculate_percentage(self.__get_moisture_raw(self.__chans[pin]))

    def get_all_moistures_percent(self):
        if not self.__connected:
            LOG.critical("I2C Bus not connected!")
            return None

        if len(self.__chans) == 0:
            LOG.critical("No channels available!")
            return None 

        results = []
        for pin in self.__chans.keys():
            results.append(self.__calculate_percentage(self.__get_moisture_raw(self.__chans[pin])))
        return results

    def get_moisture_raw(self, pin: int):        
        if not self.__connected:
            LOG.critical("I2C Bus not connected!")
            return None

        if pin not in self.__chans.keys():
            LOG.critical("No channel found on pin: {}".format(pin))
            return None

        try:
            return self.__chans[pin].value
        except Exception as ex:
            raise ex

    def __get_moisture_raw(self, chan: AnalogIn):
        if self.__connected:
            try:
                return chan.value
            except Exception as ex:
                raise ex
        else:
            return None

    def __calculate_percentage(self, raw_value):
        percentage = abs((raw_value - self.low_limit) / (self.high_limit - self.low_limit)) * 100
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        return round(percentage, 3)

    def __parse_pins(self):
        pins_str = str(utils.get_setting('soilMoisture/pins'))
        if pins_str == "":
            return []
        else:
            str_array = pins_str.split(",")
            int_array = [int(x) for x in str_array]
            return int_array
