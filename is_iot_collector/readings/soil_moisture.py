import logging
from is_iot_collector.adc import ADC
from is_iot_collector.settings import Settings

class SoilMoisture:
    def __init__(self, settings: Settings, adc: ADC):
        self.__settings = settings
        self.__adc = adc
        self.__pins = self.__settings.get('soilMoisture/pins')
        self.__low_limits = self.__settings.get('soilMoisture/lowLimits')
        self.__high_limits = self.__settings.get('soilMoisture/highLimits')

        if self.__pins is None:
            logging.critical("Invalid pin configuration!")

        for pin in self.__pins:
            try:
                self.__adc.register_pin(pin)
            except Exception as e:
                logging.critical(e)

    def percent_value_by_pin(self, pin: int):
        if pin not in self.__pins:
            logging.critical("Invalid pin: {}".format(pin))
            return None

        try:
            return self.__calculate_percentage(self.__adc.raw_value_by_pin(pin), pin)
        except Exception as ex:
            logging.error(ex)
            return None

    def percent_all_values(self):
        results = []
        try:
            for pin in self.__pins:
                results.append(self.__calculate_percentage(self.__adc.raw_value_by_pin(pin), pin))
            return results
        except Exception as ex:
            logging.error(ex)
            return None

    def raw_value_by_pin(self, pin: int):
        if pin not in self.__pins:
            logging.critical("Invalid pin: {}".format(pin))
            return None

        try:
            return self.__adc.raw_value_by_pin(pin)
        except Exception as ex:
            logging.error(ex)
            return None

    def __calculate_percentage(self, raw_value, pin):
        percentage = abs((raw_value - self.__low_limits[pin]) / (self.__high_limits[pin] - self.__low_limits[pin])) * 100
        if percentage > 100:
            percentage = 100
        return round(percentage, 3)
