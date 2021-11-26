import xml.etree.ElementTree as ET
import glob
import re
import pathlib

def getSetting(setting: str):
    file = open("/home/pi/IrrigationSystemIoT/setup.xml")
    tree = ET.parse(file)
    root = tree.getroot() 
    result = root.iter(setting)
    return next(result).text

def find_next_output_file():
    if pathlib.Path(__file__).parent.parent.joinpath("outputs").exists() == False:
        pathlib.Path(__file__).parent.parent.joinpath("outputs").mkdir()
    
    filepath = pathlib.Path(__file__).parent.parent.joinpath("outputs")
    number = 0
    numbers = list()
    for file in glob.iglob('outputs/*', recursive=True):
        x = re.search("outputs\\/output([0-9]+).txt", file)
        if x == None:
            break
        numbers.append(int(x.groups()[0]))

    if numbers.count != 0:
        number = max(numbers) + 1
    
    return filepath.joinpath("output{}.txt".format(number))