import time
import utils
import json_builder
import soil_moisture
import air_properties
import light_intensity
import local_tinydb
import mqtt_publisher as mqtt
from logger import LOG

def main():
    soil = soil_moisture.SoilMoisture()
    air = air_properties.AirProperties()
    light = light_intensity.LightIntensity()
    mqtt_client = mqtt.MQTTPublisher()
    tinyDB = local_tinydb.LocalTinyDB()
    reading_time = int(utils.get_setting('readingTime'))
    register_time = int(utils.get_setting('registerTime'))
    register_expires_at = time.time() + register_time

    output_file = utils.find_next_output_file()

    while(True):
        if time.time() > register_expires_at:
            mqtt_client.register()
            register_expires_at = time.time() + register_time

        jdata = json_builder.JsonBuilder()
        moisture = soil.percent_all_values()
        if moisture != None:
            jdata.add_key(json_builder.KeyType.SOIL_MOISTURE, moisture)

        air_hum = air.get_humidity()
        if air_hum != None:
            jdata.add_key(json_builder.KeyType.AIR_HUMIDITY, air_hum)

        air_temp = air.get_temperature()
        if air_temp != None:
            jdata.add_key(json_builder.KeyType.AIR_TEMPERATURE, air_temp)

        light_int = light.percent_value()
        if light_int != None:
            jdata.add_key(json_builder.KeyType.LIGHT_INTENSITY, light_int)

        jdata.add_timestamp()
        output = jdata.dumps()

        tinyDB.insert(output)

        LOG.info(output)
        f = open(output_file, "a")
        f.write(output + "\n")
        f.close()

        if tinyDB.is_valid(output):
            mqtt_client.publish(output)

        time.sleep(reading_time)

if __name__ == "__main__":
    main()
