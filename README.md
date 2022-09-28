# is-iot-collector

This repository represents the collector module of an IoT Irrigation System that:
1. Collects data from the field and sends it to the sink module via MQTT.

### System requirements
The application was developed on Raspberry Pi Zero W/Zero W 2 with Raspbian Buster as operating system, written in Python3.7. 

### Electric connections
![collector-electric](https://user-images.githubusercontent.com/51260103/178805085-dc51ea45-6ad1-43d8-a8eb-09392ef2a30c.jpg)
  1. 2x Capacitive Soil Moisture Sensors -> [source](https://www.amazon.com/Gikfun-Capacitive-Corrosion-Resistant-Detection/dp/B07H3P1NRM)
  2. 1x DHT22 Air Temperature and Humidity -> [source](https://www.amazon.com/HiLetgo-Temperature-Humidity-Electronic-Practice/dp/B0795F19W6/ref=sr_1_3?keywords=dht22&qid=1657737065&sr=8-3)
  3. 1x DIY Light Intensity Sensor
  ![LDR](https://user-images.githubusercontent.com/51260103/178808536-c2a7e598-0080-486c-b2e6-be6790812f13.jpg)
  4. 1x ADS1015 Analog To Digital Converter -> [source](https://www.amazon.com/Comidox-channel-Development-Programmable-Amplifier/dp/B07KW2QZS2/ref=sr_1_4?crid=11S1RP1SKMJOI&keywords=ads1015&qid=1657738141&sprefix=ads101%2Caps%2C217&sr=8-4)
 
### Install prerequisites
```
sudo apt-get update
sudo apt-get install git python3-pip python3-venv
```

### Clone repository
```
cd ~/ && git clone https://github.com/pdany1116/is-iot-collector.git
cd is-iot-collector
```

### Create virtual environment and activate
```
python3 -m venv env
source env/bin/activate
```

### Install requirements packages
```
pip install -r requirements.txt
```

### Configure enviroment variables
#### Change default values
```
cp .env.example .env
nano .env
```
`Note: Replace the environment variables with your values. All variables need to be defined!!!`
#### Export environment variables
```
set -o allexport; source .env; set +o allexport
```

### Configure system setup
```
nano setup.yml
```

### Configure python path
```
export PYTHONPATH=$(pwd):${PYTHONPATH}
```

### Configure project path
```
export PROJECT_PATH=$(pwd)
```

### Run main
```
python3 is-iot-collector/main.py
```
