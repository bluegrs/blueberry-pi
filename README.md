# Blueberry-Pi
Mobile gesture recognition glove to send hand orientation data to the Unity Engine over a Wi-Fi network.

## Hardware
Raspberry Pi 3 B+

LSM303DLHC: 3-axis accelerometer and 3-axis magnetometer

L3GD20: 3-axis gyroscope

## SW/HW Block Diagram

**Client-side:** The Raspberry-Pi interfaces with the 9-DOF sensor pack through the Client-side Data Acquisition processes and stores the received data into the respected sensor FIFOs to be accessed by the Data Formatter Process. The Data Formatter Process will frame the data according to the determined protocol and send the data to the server using the Wi-Fi module.

**Server-side:** The server-side (PC) will be running the blueberry-pi modules to interface with the videogame/simulation modules in the Dark Blue Sky project. The Wi-Fi process will immediately store the received packets into the Rx Data FIFO to be handled by the Data Formatter Process. The Data Formatter Process decodes the received packets and sends them to the Unity Input Manager using the desired format.

![software_modules](https://user-images.githubusercontent.com/40513675/58389317-849c5b80-7ff7-11e9-9c26-4210e3a6e92f.jpg)

[**Gliffy Generator Location: SW/HW Block Diagram**](https://github.com/bluegrs/blueberry-pi/tree/server/docs/gliffy)

## Contributors
Daniel Hamilton [**(@sweatpantsdanny)**](https://github.com/sweatpantsdanny)
