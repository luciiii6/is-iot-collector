import time
import utils
import json_builder
import soil_moisture
import air_properties
import local_tinydb
import mqtt_publisher as mqtt
from logger import LOG

def main():
    soil = soil_moisture.SoilMoisture()
    air = air_properties.AirProperties()
    mqtt_client = mqtt.MQTTPublisher()
    tinyDB = local_tinydb.LocalTinyDB()
    reading_time = utils.get_setting('readingTime')

    output_file = utils.find_next_output_file()
    mqtt_client.register()

    while(True):
        jdata = json_builder.JsonBuilder()
        moisture = soil.get_all_moistures_percent()
        if moisture != None:
            jdata.add_key(json_builder.KeyType.SOIL_MOISTURE, moisture)

        try:
            air_hum = air.get_humidity()
            if air_hum != None:
                jdata.add_key(json_builder.KeyType.AIR_HUMMIDITY, air_hum)
        except:
            pass

        try:
            air_temp = air.get_temperature()
            if air_temp != None:
                jdata.add_key(json_builder.KeyType.AIR_TEMPERATURE, air_temp)
        except:
            pass

        jdata.add_timestamp()
        output = jdata.dumps()

        tinyDB.insert(output)

        LOG.info(output)
        f = open(output_file, "a")
        f.write(output + "\n")
        f.close()

        if tinyDB.is_valid(output):
            mqtt_client.publish(output)

        time.sleep(int(reading_time))

if __name__ == "__main__":
    main()
