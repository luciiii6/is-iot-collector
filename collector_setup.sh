#!/bin/bash
sudo touch /usr/local/bin/startup_collector.sh
sudo chmod u+x /usr/local/bin/startup_collector.sh
sudo echo "#!/bin/bash" | sudo tee -a /usr/local/bin/startup_collector.sh
sudo echo "cd /home/pi/is-iot-collector" | sudo tee -a /usr/local/bin/startup_collector.sh
sudo echo "source env/bin/activate" | sudo tee -a /usr/local/bin/startup_collector.sh
sudo echo "export PYTHONPATH=$(pwd):${PYTHONPATH}" | sudo tee -a /usr/local/bin/startup_collector.sh
sudo echo "export PROJECT_PATH=$(pwd)" | sudo tee -a /usr/local/bin/startup_collector.sh
sudo echo "python is_iot_collector/main.py" | sudo tee -a /usr/local/bin/startup_collector.sh
#copy the service file to be started by systemd
sudo cp collector.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable collector.service