import time
import utils
import soil_moisture
import air_properties
import mqtt_client
from datetime import datetime

def main():
    soil = soil_moisture.SoilMoisture()
    air = air_properties.AirProperties()
    mqttclient = mqtt_client.MQTTClient()
    reading_time = utils.getSetting('readingTime')
    air_temp = '-'
    air_hum = '-'

    output_file = utils.find_next_output_file()

    f = open(output_file, "a")
    f.write("Time Stamp,Soil Moisture[0],Soil Moisture[1],Air Temperature,Air Humidity\n")
    f.close()

    while(True):
        soil_temp = soil.get_moisture_pct()

        try:
            air_hum = air.get_humidity()
        except Exception as ex:
            air_hum = '-'

        try:
            air_temp = air.get_temperature()
        except Exception as ex:
            air_temp = '-'

        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")

        output = "{},{}%,{}%,{}C,{}%\n".format(current_time, soil_temp[0], soil_temp[1], air_temp, air_hum)
        print(output)
        f = open(output_file, "a")
        f.write(output)
        f.close()
        time.sleep(reading_time)

if __name__ == "__main__":
    main()
