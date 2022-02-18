import xml.etree.ElementTree as ET
from logger import LOG
import glob
import re
import pathlib

def get_setting(setting: str):
    try:
    file = open("./setup.xml")
    tree = ET.parse(file)
    except:
        LOG.err("Invalid configuration file! {}".format(file.name))
        return
    root = tree.getroot() 
    if setting.startswith("./") == False:
        setting = "./" + setting
    return root.findall(setting)[0].text

def get_settings(settings: str):
    try:
    file = open("./setup.xml")
    tree = ET.parse(file)
    except:
        LOG.err("Invalid configuration file! {}".format(file.name))
        return
    root = tree.getroot() 
    if settings.startswith("./") == False:
        settings = "./" + settings
    results = []
    for setting in list(root.find(settings)):
        results.append(setting.text)
    return results

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