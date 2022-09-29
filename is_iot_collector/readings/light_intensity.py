import logging
from is_iot_collector.adc import ADC
from is_iot_collector.settings import Settings

class LightIntensity:
    def __init__(self, settings: Settings, adc: ADC):
        self.__settings = settings
        self.__adc = adc
        self.__pin = self.__settings.get('lightIntensity/pin')

        try:
            self.__adc.register_pin(self.__pin)
        except Exception as e:
            logging.critical(e)
        
        self.__low_limit = self.__settings.get('lightIntensity/lowLimit')
        self.__high_limit = self.__settings.get('lightIntensity/highLimit')

    def percent_value(self):
        try:
            percentage = self.__calculate_percentage(self.__adc.raw_value_by_pin(self.__pin))
            if percentage == 100:
                return None

            return percentage
        except Exception as ex:
            logging.error(ex)
            return None

    def raw_value(self):
        try:
            return self.__adc.raw_value_by_pin(self.__pin)
        except Exception as ex:
            logging.error(ex)
            return None
        
    def __calculate_percentage(self, raw_value):
        percentage = abs((raw_value - self.__low_limit) / (self.__high_limit - self.__low_limit)) * 100
        if percentage > 100:
            percentage = 100
        return round(percentage, 3)
