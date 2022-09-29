import os
import time
import logging
import threading
from threading import Lock
from is_iot_collector.adc import ADC
from is_iot_collector.json_builder import *
from is_iot_collector.settings import Settings
from is_iot_collector.local_tinydb import LocalTinyDB
from is_iot_collector.mqtt.mqtt_client import MQTTClient
from is_iot_collector.readings.soil_moisture import SoilMoisture
from is_iot_collector.readings.air_properties import AirProperties
from is_iot_collector.readings.light_intensity import LightIntensity

class Collector:
    def __init__(self, settings=None):
        if settings == None:
            self.__settings_mutex = Lock()
            self.__settings = Settings(os.getenv('PROJECT_PATH') + '/setup.yml', self.__settings_mutex)
        else:
            self.__settings = settings

        self.__adc = ADC()
        self.__air_properties = AirProperties()
        self.__soil_moisture = SoilMoisture(self.__settings, self.__adc)
        self.__light_intensity = LightIntensity(self.__settings, self.__adc)
        self.__mqtt_client = MQTTClient(self.__settings)
        self.__local_tiny_db = LocalTinyDB(self.__settings)
        self.__reading_time = self.__settings.get('readingTime')
        self.__register_time = self.__settings.get('registerTime')
        self.__register_expires_at = time.time() + self.__register_time
        self.__thread = threading.Thread(target = self.__run, daemon = True)

    def start(self):
        logging.info("Collector application started.")
        self.__running = True
        self.__thread.start()

    def stop(self):
        self.__running = False
        self.__thread.join()
        logging.info("Collector application stopped.")

    def status(self):
        return self.__running and self.__thread.is_alive()

    def __run(self):
        while self.__running:
            if time.time() > self.__register_expires_at:
                self.__mqtt_client.register()
                self.__register_expires_at = time.time() + self.__register_time

            if  self.__settings.get('sinkId') == 'default':
                continue

            payload = JsonBuilder(self.__settings)
            soil_moisture = self.__soil_moisture.percent_all_values()
            if soil_moisture:
                payload.add_key(KeyType.SOIL_MOISTURE, soil_moisture)

            air_humidity = self.__air_properties.humidity()
            if air_humidity:
                payload.add_key(KeyType.AIR_HUMIDITY, air_humidity)

            air_temperature = self.__air_properties.temperature()
            if air_temperature:
                payload.add_key(KeyType.AIR_TEMPERATURE, air_temperature)

            light_intensity = self.__light_intensity.percent_value()
            if light_intensity:
                payload.add_key(KeyType.LIGHT_INTENSITY, light_intensity)

            payload.add_timestamp()
            json_payload = payload.to_json()

            self.__local_tiny_db.insert(json_payload)

            logging.info(json_payload)

            if self.__local_tiny_db.is_valid(json_payload):
                self.__mqtt_client.publish(json_payload)

            timeout = self.__reading_time
            while timeout > 0:
                timeout -= 1
                time.sleep(1)
                if not self.__running:
                    return
