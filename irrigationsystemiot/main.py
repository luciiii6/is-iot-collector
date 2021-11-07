import time
import utils
import weather
import soil_moisture
import air_properties

def main():
    soil = soil_moisture.SoilMoisture()
    air = air_properties.AirProperties()
    w = weather.Weather(utils.getSetting('latitude'), utils.getSetting('longitude'))

    while(True):
        print("Soil Moisture: {:>5}%".format(soil.get_moisture_pct()))
        
        try:
            print("Temp: {} C    Humidity: {}% ".format(air.get_temperature(), air.get_humidity()))
        except Exception as ex:
            print(str(ex))

        time.sleep(1)

if __name__ == "__main__":
    main()