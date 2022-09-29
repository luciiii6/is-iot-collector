from is_iot_collector.settings import Settings
from is_iot_collector.mqtt.mqtt_client import MQTTClient
import json
from is_iot_collector.errors.air_humidity_error import AirHumidityError
from is_iot_collector.errors.air_temperature_error import AirTemperatureError
from is_iot_collector.errors.light_intensity_error import LightIntensityError
from is_iot_collector.errors.soil_moisture_error import SoilMoistureError


class ErrorHandler:
    NONE_READINGS_VALUE = 100
    def __init__(self, mqtt_client,  settings = Settings()):
        self.__errors = [AirHumidityError(), AirTemperatureError(), LightIntensityError(), SoilMoistureError()]
        self.__settings = settings
        self.__mqtt_client = mqtt_client
        self.__number_detected_errors = 0

    def check_values(self):
        error_message = ''
        if self.__number_detected_errors > 0:
            for error in self.__errors:
                error_message = error.build_message(error_message)
                error.error_sent = True

            error_message = json.dumps({collectorId: self.__settings.get('id'), errors: error_message})
            self.__mqtt_client.send_errors(error_message)

    def increment_air_humidity_error(self):
        self.__errors[0].counter+= 1

        if self.__errors[0].counter == NONE_READINGS_VALUE:
            self.__number_detected_errors += 1

    def increment_air_temperature_error(self):
        self.__errors[1].counter += 1

        if self.__errors[1].counter == NONE_READINGS_VALUE:
            self.__number_detected_errors += 1

    def increment_soil_moisture_error(self):
        self.__errors[3].counter += 1

        if self.__errors[3].counter == NONE_READINGS_VALUE:
            self.__number_detected_errors += 1


    def increment_light_intensity_error(self):
        self.__errors[2].counter+= 1

        if self.__errors[2].counter == NONE_READINGS_VALUE:
            self.__number_detected_errors += 1


    def reset_air_humidity(self):
        self.__errors[0].reset_counter()
        self.__errors[0].reset_flag()

    def reset_air_temperature(self):
        self.__errors[1].reset_counter()
        self.__errors[1].reset_flag()

    def reset_light_intensity(self):
        self.__errors[2].reset_counter()
        self.__errors[2].reset_flag()

    def reset_soil_moisture(self):
        self.__errors[3].reset_counter()
        self.__errors[3].reset_flag()