import time
import utils
import json_builder
import soil_moisture
import air_properties
import mqtt_publisher as mqtt
from datetime import datetime

def main():
    soil = soil_moisture.SoilMoisture()
    air = air_properties.AirProperties()
    mqtt_client = mqtt.MQTTPublisher()
    reading_time = utils.get_setting('readingTime')
    air_temp = '-'
    air_hum = '-'

    output_file = utils.find_next_output_file()

    f = open(output_file, "a")
    f.write("Time Stamp,Soil Moisture[0],Soil Moisture[1],Air Temperature,Air Humidity\n")
    f.close()

    mqtt_client.register()

    while(True):
        jdata = json_builder.JsonBuilder()
        moisture = soil.get_all_moistures_percent()
        if moisture != None:
            jdata.add_key(json_builder.KeyType.SOIL_MOISTURE, moisture)

        try:
            air_hum = air.get_humidity()
            jdata.add_key(json_builder.KeyType.AIR_HUMMIDITY, air_hum)
        except:
            pass

        try:
            air_temp = air.get_temperature()
            jdata.add_key(json_builder.KeyType.AIR_TEMPERATURE, air_temp)
        except:
            pass

        jdata.add_timestamp()

        output = jdata.dumps()
        print(output)
        f = open(output_file, "a")
        f.write(output + "\n")
        f.close()
        mqtt_client.publish(output)
        time.sleep(int(reading_time))

if __name__ == "__main__":
    main()
