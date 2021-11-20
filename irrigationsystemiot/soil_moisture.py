import board
import busio
import utils
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class SoilMoisture:
    def __init__(self):
        self.__i2c = busio.I2C(board.SCL, board.SDA)
        self.__ads = ADS.ADS1015(self.__i2c)
        self.__chan0 = AnalogIn(self.__ads, ADS.P0)
        self.__chan1 = AnalogIn(self.__ads, ADS.P1)
        self.low_limit = int(utils.getSetting('lowLimit'))
        self.high_limit = int(utils.getSetting('highLimit'))

    def get_moisture_pct(self, chan = None):
        if chan == None:
            return self.__calculate_percentage(self.get_moisture_raw(0)), self.__calculate_percentage(self.get_moisture_raw(1))
        if isinstance(chan, int):
            return self.__calculate_percentage(self.get_moisture_raw(chan))

    def get_moisture_raw(self, chan: int):
        ads_chan = None
        if chan == 0:
            ads_chan = self.__chan0
        elif chan == 1:
            ads_chan = self.__chan1
        else:
            raise ValueError("Invalid channel number!")

        try:
            return ads_chan.value
        except Exception as ex:
            raise ex

    def __calculate_percentage(self, raw_value):
        percentage = abs((raw_value - self.low_limit) / (self.high_limit - self.low_limit)) * 100
        if percentage < 0:
            percentage = 0
        if percentage > 100:
            percentage = 100
        return round(percentage, 3)