import time
import utils
import yaml
import logging
import logging.config
from is_iot_collector.readings.soil_moisture import soil_moisture
from is_iot_collector.readings.air_properties import air_properties
from is_iot_collector.readings.light_intensity import light_intensity
from is_iot_collector.mqtt.mqtt_publisher import mqtt_client
from is_iot_collector.local_tinydb import tiny_db
from is_iot_collector.json_builder import *


def init_logger(file_path: str):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f.read())

    logging.config.dictConfig(config)


def main():
    init_logger('../logger_config.yml')
    reading_time = int(utils.get_setting('readingTime'))
    register_time = int(utils.get_setting('registerTime'))
    register_expires_at = time.time() + register_time

    output_file = utils.find_next_output_file()

    while True:
        if time.time() > register_expires_at:
            mqtt_client.register()
            register_expires_at = time.time() + register_time

        jdata = JsonBuilder()
        moisture = soil_moisture.percent_all_values()
        if moisture is not None:
            jdata.add_key(KeyType.SOIL_MOISTURE, moisture)

        air_hum = air_properties.humidity()
        if air_hum is not None:
            jdata.add_key(KeyType.AIR_HUMIDITY, air_hum)

        air_temp = air_properties.temperature()
        if air_temp is not None:
            jdata.add_key(KeyType.AIR_TEMPERATURE, air_temp)

        light_int = light_intensity.percent_value()
        if light_int is not None:
            jdata.add_key(KeyType.LIGHT_INTENSITY, light_int)

        jdata.add_timestamp()
        output = jdata.dumps()

        tiny_db.insert(output)

        LOG.info(output)
        f = open(output_file, "a")
        f.write(output + "\n")
        f.close()

        if tiny_db.is_valid(output):
            mqtt_client.publish(output)

        time.sleep(reading_time)


if __name__ == "__main__":
    main()
