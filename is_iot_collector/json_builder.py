import json
import time
from enum import Enum
from is_iot_collector.settings import Settings

class KeyType(Enum):
    SOIL_MOISTURE = 0
    AIR_HUMIDITY = 1
    AIR_TEMPERATURE = 2
    LIGHT_INTENSITY = 3

class JsonBuilder:
    def __init__(self, settings: Settings):
        self.__settings = settings
        self.__data = {}
        self.__data['collectorId'] = self.__settings.get('id')
    
    def add_timestamp(self):
        if 'date' in self.__data:
            return
        now = time.time()
        self.__data['timestamp'] = now
        return

    def add_key(self, key: KeyType, value):
        key_str = ''
        if key == KeyType.SOIL_MOISTURE:
            key_str = 'soilMoisture'
        elif key == KeyType.AIR_HUMIDITY:
            key_str = 'airHumidity'
        elif key == KeyType.AIR_TEMPERATURE:
            key_str = 'airTemperature'
        elif key == KeyType.LIGHT_INTENSITY:
            key_str = 'lightIntensity'
        else:
            return

        if key_str in self.__data:
            return

        self.__data[key_str] = value

    def to_json(self):
        return json.dumps(self.__data)

