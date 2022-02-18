import json
from datetime import datetime
import utils
from enum import Enum

class KeyType(Enum):
    SOIL_MOISTURE = 0
    AIR_HUMMIDITY = 1
    AIR_TEMPERATURE = 2
    LIGHT_INTENSITY = 3

class JsonBuilder:
    def __init__(self):
        self.__data = {}
        self.__data['collectorId'] = utils.get_setting('name')[9:]
    
    def add_timestamp(self):
        if ('date' in self.__data):
            return
        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")
        self.__data['date'] = current_time
        return

    def add_key(self, key: KeyType, value):
        key_str = ''
        if key == KeyType.SOIL_MOISTURE:
            key_str = 'soilMoisture'
        elif key == KeyType.AIR_HUMMIDITY:
            key_str = 'airHummidity'
        elif key == KeyType.AIR_TEMPERATURE:
            key_str = 'airTemperature'
        elif key == KeyType.LIGHT_INTENSITY:
            key_str = 'lightIntensity'
        else:
            return

        if (key_str in self.__data):
            return

        self.__data[key_str] = value

    def dumps(self):
        return json.dumps(self.__data)

