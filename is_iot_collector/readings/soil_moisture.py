import utils
import logging
from adc import adc

class SoilMoisture:
    def __init__(self):
        self.__pins = self.__parse_pins()
        if len(self.__pins) == 0:
            logging.critical("Invalid pin configuration!")

        for pin in self.__pins:
            try:
                adc.register_pin(pin)
            except Exception as e:
                logging.critical(e)
        self.__parse_limits()

    def percent_value_by_pin(self, pin: int):
        if pin not in self.__pins:
            logging.critical("Invalid pin: {}".format(pin))
            return None

        try:
            return self.__calculate_percentage(adc.raw_value_by_pin(pin), pin)
        except Exception as ex:
            logging.error(ex)
            return None

    def percent_all_values(self):
        results = []
        try:
            for pin in self.__pins:
                results.append(self.__calculate_percentage(adc.raw_value_by_pin(pin), pin))
            return results
        except Exception as ex:
            logging.error(ex)
            return None

    def raw_value_by_pin(self, pin: int):
        if pin not in self.__pins:
            logging.critical("Invalid pin: {}".format(pin))
            return None

        try:
            return adc.raw_value_by_pin(pin)
        except Exception as ex:
            logging.error(ex)
            return None

    def __calculate_percentage(self, raw_value, pin):
        percentage = abs((raw_value - self.low_limits[pin]) / (self.high_limits[pin] - self.low_limits[pin])) * 100
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

    def __parse_limits(self):
        low_limits_str=str(utils.get_setting('soilMoisture/lowLimits'))
        high_limits_str=str(utils.get_setting('soilMoisture/highLimits'))
        if low_limits_str == "":
            return []
        else:
            str_array = low_limits_str.split(",")
            self.low_limits = [int(x) for x in str_array]

        if high_limits_str == "":
            return []
        else:
            str_array = high_limits_str.split(",")
            self.high_limits = [int(x) for x in str_array]

soil_moisture = SoilMoisture()
