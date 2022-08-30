import utils
from logger import LOG
from adc import adc

class LightIntensity:
    def __init__(self):
        self.__pin = int(utils.get_setting('lightIntensity/pin'))

        try:
            adc.register_pin(self.__pin)
        except Exception as e:
            LOG.critical(e)
        
        self.low_limit = int(utils.get_setting('lightIntensity/lowLimit'))
        self.high_limit = int(utils.get_setting('lightIntensity/highLimit'))

    def percent_value(self):
        try:
            return self.__calculate_percentage(adc.raw_value_by_pin(self.__pin))
        except Exception as ex:
            LOG.err(ex)
            return None

    def raw_value(self):
        try:
            return adc.raw_value_by_pin(self.__pin)
        except Exception as ex:
            LOG.err(ex)
            return None
        
    def __calculate_percentage(self, raw_value):
        percentage = abs((raw_value - self.low_limit) / (self.high_limit - self.low_limit)) * 100
        if percentage > 100:
            percentage = 100
        return round(percentage, 3)

light_intensity = LightIntensity()
