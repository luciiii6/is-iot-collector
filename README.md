# (Work In Progress) is-iot-collector

### System requirements
The application was developed on Raspberry Pi Zero W/Zero W 2 with Raspbian Buster as operating system, written in Python3.7. 

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

### Configure system setup
```
nano setup.xml
```

### Configure python path
```
export PYTHONPATH=$(pwd):${PYTHONPATH}
```

### Run main
```
python3 is-iot-collector/main.py
```
