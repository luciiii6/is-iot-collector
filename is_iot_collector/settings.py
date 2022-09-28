import yaml
import dpath.util
from threading import Lock

class Settings:
    def __init__(self, filepath, mutex: Lock):
        file = open(filepath)
        self.__settings = yaml.safe_load(file)
        self.__mutex = mutex

    def get(self, name):
        try:
            with self.__mutex:
                value = dpath.util.get(self.__settings, name)
        except (ValueError, KeyError):
            value = None

        return value

    def set(self, name, value):
        with self.__mutex:
            dpath.util.set(self.__settings, name, value)

