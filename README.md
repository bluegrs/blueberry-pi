# Blueberry-Pi

>Mobile gesture recognition glove to send hand orientation data to the Unity Engine over a Wi-Fi network.

## SW/HW Block Diagram

**Server-side** 

> The Raspberry-Pi is expected to run the _device.py_ script. The Raspberry-Pi interfaces with the 9-DOF sensor pack with the NXP module. The server Wi-Fi module immediately sends the data to the network through a TCP packet formatted in json string.

**Client-side** 

> The client-side (PC) will be running the Unity simulation located in blueberry-pi/sim. The Wi-Fi module will immediately store the received packets into a string FIFO to be parsed and stored into the float FIFOs for sensor data. The player movement module will read from the sensor FIFO and create movements in the simulation accordingly.  

![blueberry](https://user-images.githubusercontent.com/40513675/60064552-c3910000-96ce-11e9-8f74-6d49027b9dc7.png)

[**Gliffy Generator Location: SW/HW Block Diagram**](https://github.com/bluegrs/blueberry-pi/tree/server/docs/gliffy)

## Hardware

> Raspberry Pi Zero W
>
> LSM303DLHC (_3-axis accelerometer and 3-axis magnetometer_)
>
> L3GD20 (_3-axis gyroscope_)

## Dependencies
> [**Python 3 (3.6+)**](https://www.python.org/downloads/)
>
> [**Adafruit FXOS8700 Python 3 Module**](https://github.com/adafruit/Adafruit_CircuitPython_FXOS8700)
>
> [**Adafruit FXAS21002C Python 3 Module**](https://github.com/adafruit/Adafruit_CircuitPython_FXAS21002C)

## Setting up the Raspberry-Pi

> Run the following commands in a Raspi terminal to update the OS.

```
sudo apt-get update

sudo apt-get upgrade

sudo apt-get install python3-pip
```
> Install the kernel support for I2C in the software configuration tool under _Interfacing Options_.

```
sudo apt-get install -y python-smbus

sudo apt-get install -y i2c-tools

sudo raspi-config

sudo reboot
```

> Install the Adafruit Python library for the sensors and some other useful Python libraries.

```
sudo pip3 install adafruit-circuitpython-fxos8700

sudo pip3 install adafruit-circuitpython-fxas21002c

pip3 install RPI.GPIO

pip3 install adafruit-blinka
```

## Contributors
>Daniel Hamilton [**(@sweatpantsdanny)**](https://github.com/sweatpantsdanny)
