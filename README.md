In a small project I installed a Raspberry Pi and LED strips include the power supply as desk lighting in a LACK shelf from IKEA. To monitor the temperature in the shelf, I also installed a temperature sensor. The temperature and the temperature of the Raspberry Pi must be monitored. For this I created this small script to transfer the data via MQTT.

The script is configured for the following hardware:
- Raspberry Pi 2
- 1Wire Sensor DS18B20
