import board
import busio
import utils
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class SoilMoisture:
    def __init__(self):
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.__ads = ADS.ADS1015(self.__i2c)
        self.__chan = AnalogIn(self.__ads, ADS.P0)
        self.low_limit = int(utils.getSetting('lowLimit'))
        self.high_limit = int(utils.getSetting('highLimit'))

    def get_moisture_pct(self):
        try:
            return self.__calculate_percentage(self.__chan.value)
        except Exception as ex:
            raise ex

    def get_moisture_raw(self):
        try:
            return self.__chan.value
        except Exception as ex:
            raise ex

    def __calculate_percentage(self, raw_value):
        percentage = abs((raw_value - self.low_limit) / (self.high_limit - self.low_limit)) * 100
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        return round(percentage, 3)