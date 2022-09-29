from is_iot_collector.settings import Settings
from is_iot_collector.mqtt.mqtt_client import MQTTClient
import json

class ErrorHandler:
    NONE_READINGS_VALUE = 100
    def __init__(self, mqtt_client,  settings = Settings()):
        self.__air_humidity_counter = 0
        self.__air_temperature_counter = 0
        self.__light_intensity_counter = 0
        self.__soil_moisture_counter = 0
        self.__settings = settings
        self.__mqtt_client = mqtt_client
        self.__sensors_with_error = []
        self.__errors_already_sent = False

    def check_values(self):
        error_message = ''
        if len(self.__sensors_with_error) > 0 and not self.__errors_already_sent:
            for error in self.__sensors_with_error:
                error_message += error + "\n"

            self.__mqtt_client.send_errors(error_message)
            self.__sensors_with_error = []
            self.__errors_already_sent = True

    def increment_air_humidity_error(self):
        self.__air_humidity_counter += 1

        if self.__air_humidity_counter == NONE_READINGS_VALUE:
            self.__sensors_with_error.append('Air humidity sensor has a problem')


    def increment_air_temperature_error(self):
        self.__air_temperature_counter += 1

        if self.__air_temperature_counter == NONE_READINGS_VALUE:
            self.__sensors_with_error.append('Air temperature sensor has a problem')


    def increment_soil_moisture_error(self):
        self.__soil_moisture_counter += 1

        if self.__soil_moisture_counter == NONE_READINGS_VALUE:
            self.__sensors_with_error.append('Soil moisture sensor has a problem')


    def increment_light_intensity_error(self):
        self.__air_humidity_counter += 1

        if self.__light_intensity_counter == NONE_READINGS_VALUE:
            self.__sensors_with_error.append('Light intensity sensor has a problem')

    def __reset_flag_for_sent_errors(self):
        self.__errors_already_sent = False

    def reset_air_humidity(self):
        self.__air_humidity_counter = 0
        self.__reset_flag_for_sent_errors()

    def reset_air_temperature(self):
        self.__air_temperature_counter = 0
        self.__reset_flag_for_sent_errors()
    def reset_light_intensity(self):
        self.__light_intensity_counter = 0
        self.__reset_flag_for_sent_errors()
    def reset_soil_moisture(self):
        self.__soil_moisture_counter = 0
        self.__reset_flag_for_sent_errors()