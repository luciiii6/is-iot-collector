import time
import json
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

max_val = None
min_val = None
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P2)
baseline_check = input("Is Light Sensor Covered? (enter 'y' to proceed): ")

if baseline_check == 'y':
    max_val = chan.value
print("------{:>5}\t{:>5}".format("raw", "v"))

for x in range(0, 10):
    if chan.value > max_val:
        max_val = chan.value
    print("CHAN 2: "+"{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(0.5)

print('\n')

water_check = input("Does the Light Sensor receive the maximum light? (enter 'y' to proceed): ")
if water_check == 'y':
    min_val = chan.value

print("------{:>5}\t{:>5}".format("raw", "v"))
for x in range(0, 10):
    if chan.value < min_val:
        min_val = chan.value
    print("CHAN 2: "+"{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    time.sleep(0.5)


config_data = dict()
config_data["min"] = min_val
config_data["max"] = max_val
with open('light_config.json', 'w') as outfile:
    json.dump(config_data, outfile)
print('\n')
print(config_data)
time.sleep(0.5)
