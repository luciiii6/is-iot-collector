import json
import logging
from tinydb import TinyDB, Query
from is_iot_collector.settings import Settings


class LocalTinyDB:
    def __init__(self, settings: Settings):
        self.__settings = settings
        self.__db = TinyDB(self.__settings.get('localReadings/dbName'))
        self.__count = self.__settings.get('localReadings/count')

    def insert(self, doc):
        if not isinstance(doc, dict):
            doc = json.loads(doc)

        self.__clear_readings()
        self.__db.insert(doc)

    def is_valid(self, doc):
        if not isinstance(doc, dict):
            doc = json.loads(doc)

        # Check soil moistures values
        if 'soilMoisture' in doc.keys():
            moistures = doc['soilMoisture']
            threshold = self.__settings.get('localReadings/thresholds/soilMoisture')
            readings = self.__db.all()
            for reading in readings:
                local_moistures = reading['soilMoisture']
                for i in range(0, len(local_moistures)):
                    if local_moistures[i] > moistures[i] + threshold or local_moistures[i] < moistures[i] - threshold:
                        return True

        # Check air humidity values
        if 'airHumidity' in doc.keys():
            reading = Query()
            threshold = self.__settings.get('localReadings/thresholds/airHumidity')
            set = self.__db.search(
                (reading.airHumidity > doc['airHumidity'] + threshold) |
                (reading.airHumidity < doc['airHumidity'] - threshold))
            if len(set) > 0:
                return True

        # Check air temperature values
        if 'airTemperature' in doc.keys():
            reading = Query()
            threshold = self.__settings.get('localReadings/thresholds/airTemperature')
            set = self.__db.search(
                (reading.airTemperature > doc['airTemperature'] + threshold) | 
                (reading.airTemperature < doc['airTemperature'] - threshold))
            if len(set) > 0:
                return True

        return False

    def __clear_readings(self):
        while len(self.__db) >= self.__count:
            id = self.__get_first_entry_id()
            self.__db.remove(doc_ids=[id])

    def __get_first_entry_id(self):
        return self.__db.all()[0].doc_id
