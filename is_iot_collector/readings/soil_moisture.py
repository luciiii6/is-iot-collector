import utils
from logger import LOG
from adc import adc

class SoilMoisture:
    def __init__(self):
        self.__pins = self.__parse_pins()
        if len(self.__pins) == 0:
            LOG.critical("Invalid pin configuration!")

        for pin in self.__pins:
            try:
                adc.register_pin(pin)
            except Exception as e:
                LOG.critical(e)
        
        self.low_limit = int(utils.get_setting('soilMoisture/lowLimit'))
        self.high_limit = int(utils.get_setting('soilMoisture/highLimit'))

    def percent_value_by_pin(self, pin: int):
        if pin not in self.__pins:
            LOG.critical("Invalid pin: {}".format(pin))
            return None

        try:
            return self.__calculate_percentage(adc.raw_value_by_pin(pin))
        except Exception as ex:
            LOG.err(ex)
            return None

    def percent_all_values(self):
        results = []
        try:
            for pin in self.__pins:
                results.append(self.__calculate_percentage(adc.raw_value_by_pin(pin)))
            return results
        except Exception as ex:
            LOG.err(ex)
            return None

    def raw_value_by_pin(self, pin: int):
        if pin not in self.__pins:
            LOG.critical("Invalid pin: {}".format(pin))
            return None

        try:
            return adc.raw_value_by_pin(pin)
        except Exception as ex:
            LOG.err(ex)
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

soil_moisture = SoilMoisture()