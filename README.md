# Blueberry-Pi
Mobile gesture recognition glove to send hand orientation data to the Unity Engine over a Wi-Fi network.

## SW/HW Block Diagram

**Client-side:** The Raspberry-Pi interfaces with the 9-DOF sensor pack through the Client-side Data Acquisition processes and stores the received data into the respected sensor FIFOs to be accessed by the Data Formatter Process. The Data Formatter Process will frame the data according to the determined protocol and send the data to the server using the Wi-Fi module.

**Server-side:** The server-side (PC) will be running the blueberry-pi modules to interface with the videogame/simulation modules in the Dark Blue Sky project. The Wi-Fi process will immediately store the received packets into the Rx Data FIFO to be handled by the Data Formatter Process. The Data Formatter Process decodes the received packets and sends them to the Unity Input Manager using the desired format.

![software_modules](https://user-images.githubusercontent.com/40513675/58389317-849c5b80-7ff7-11e9-9c26-4210e3a6e92f.jpg)

[**Gliffy Generator Location: SW/HW Block Diagram**](https://github.com/bluegrs/blueberry-pi/tree/server/docs/gliffy)

## Hardware
Raspberry Pi 3 B+

LSM303DLHC: 3-axis accelerometer and 3-axis magnetometer

L3GD20: 3-axis gyroscope

## Dependencies
[**Python3**](https://www.python.org/downloads/)

[**Adafruit FXOS8700 Python3 Package**](https://github.com/adafruit/Adafruit_CircuitPython_FXOS8700)

[**Adafruit FXAS21002C Python3 Package**](https://github.com/adafruit/Adafruit_CircuitPython_FXAS21002C)

## Setting up the Raspberry-Pi

Run the following commands in a Raspi terminal to update the OS.

```
sudo apt-get update

sudo apt-get upgrade

sudo apt-get install python3-pip
```
Install the kernel support for I2C in the software configuration tool under _Interfacing Options_.

```
sudo apt-get install -y python-smbus

sudo apt-get install -y i2c-tools

sudo raspi-config

sudo reboot
```

Install the Adafruit Python library for the sensors and some other useful Python libraries.

```
sudo pip3 install adafruit-circuitpython-fxos8700

sudo pip3 install adafruit-circuitpython-fxas21002c

pip3 install RPI.GPIO

pip3 install adafruit-blinka
```

## Contributors
Daniel Hamilton [**(@sweatpantsdanny)**](https://github.com/sweatpantsdanny)
