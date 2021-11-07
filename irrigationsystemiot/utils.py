import xml.etree.ElementTree as ET

def getSetting(setting):
    file = open("/home/pi/IrrigationSystemIoT/setup.xml")
    tree = ET.parse(file)
    root = tree.getroot() 
    result = root.iter(setting)
    return next(result).text