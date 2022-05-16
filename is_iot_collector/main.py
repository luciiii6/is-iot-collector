import time
import utils
from readings.soil_moisture import soil_moisture
from readings.air_properties import air_properties
from readings.light_intensity import light_intensity
from mqtt.mqtt_publisher import mqtt_client
from local_tinydb import tiny_db
from json_builder import *
from logger import LOG

def main():
    reading_time = int(utils.get_setting('readingTime'))
    register_time = int(utils.get_setting('registerTime'))
    register_expires_at = time.time() + register_time

    output_file = utils.find_next_output_file()

    while(True):
        if time.time() > register_expires_at:
            mqtt_client.register()
            register_expires_at = time.time() + register_time

        jdata = JsonBuilder()
        moisture = soil_moisture.percent_all_values()
        if moisture != None:
            jdata.add_key(KeyType.SOIL_MOISTURE, moisture)

        air_hum = air_properties.humidity()
        if air_hum != None:
            jdata.add_key(KeyType.AIR_HUMIDITY, air_hum)

        air_temp = air_properties.temperature()
        if air_temp != None:
            jdata.add_key(KeyType.AIR_TEMPERATURE, air_temp)

        light_int = light_intensity.percent_value()
        if light_int != None:
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
