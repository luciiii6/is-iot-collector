import logging
import xml.etree.ElementTree as ET


def get_setting(setting: str):
    try:
        file = open("./setup.xml")
        tree = ET.parse(file)
    except:
        logging.error("Invalid configuration file! {}".format(file.name))
        return
    root = tree.getroot() 
    if not setting.startswith("./"):
        setting = "./" + setting
    return root.findall(setting)[0].text


def get_settings(settings: str):
    try:
        file = open("./setup.xml")
        tree = ET.parse(file)
    except:
        logging.error("Invalid configuration file! {}".format(file.name))
        return
    root = tree.getroot() 
    if not settings.startswith("./"):
        settings = "./" + settings
    results = []
    for setting in list(root.find(settings)):
        results.append(setting.text)
    return results
