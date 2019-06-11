'''
CLASS DESCRIPTION:
This class reads from the accelerometer, gyro, magnetomer information.
It also includes functions to read json strings with rounded floats of the
data returned from the sensors.
'''

import json, math
import board
import busio
import adafruit_fxos8700 as fxoslib
import adafruit_fxas21002c as fxaslib
import time

class sensor:
    
    def __init__(self, precision=3):
        self.fxos = None
        self.fxas = None
        self.precision = precision

        # call the setup functions
        (self.fxos, self.fxas) = self.__SetupSensors()


    # +----------+----------+----------+----------+
    # |             PRIVATE METHODS               |
    # +----------+----------+----------+----------+
    
    '''
    SUMMARY:
    Initialize the I2C bus and the sensor backpack.

    RETURN:
    fxos - (obj) Data from the accelerometer, magnetometer
    fxas - (obj) Data from the gyroscope
    '''
    def __SetupSensors(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        fxos = fxoslib.FXOS8700(i2c, accel_range=fxoslib.ACCEL_RANGE_2G) # accelerometer, magnetometer
        fxas = fxaslib.FXAS21002C(i2c) # gyro
        return fxos, fxas
    
    
    # +----------+----------+----------+----------+
    # |              PUBLIC METHODS               |
    # +----------+----------+----------+----------+
    
    '''
    SUMMARY:
    Read raw x,y,z information from the accelerometer sensor.

    RETURN:
    x - (float) X-axis data from whichever sensor is chosen
    y - (float) Y-axis data from whichever sensor is chosen
    z - (float) Z-axis data from whichever sensor is chosen
    '''
    def accel(self):
        x,y,z = self.fxos.accelerometer
        return x,y,z

    def mag(self):
        x,y,z = self.fxos.magnetometer
        return x,y,z

    def gyro(self):
        x,y,z = self.fxas.gyroscope
        return x,y,z    

    '''
    SUMMARY:
    Read the sensor data, round to some precision, and
    return the data as a json string.

    RETURN:
    [XX.XXX, YY.YYY, ZZ.ZZZ]
    '''
    def accelj(self):
        x,y,z = self.fxos.accelerometer
        return x,y,z

    def magj(self):
        x,y,z = self.fxos.magnetometer
        return x,y,z

    def gyroj(self):
        x,y,z = self.fxas.gyroscope

        # round the data before encoding
        xround = round(x, self.precision)
        yround = round(y, self.precision)
        zround = round(z, self.precision)

        # encode the data before returning
        return json.dumps([xround, yround, zround])   

# +----------+----------+----------+----------+
# |                 TEST UNIT                 |
# +----------+----------+----------+----------+
def main():
    s = sensor()

    while True:
        accel_x, accel_y, accel_z = s.accel()
        mag_x, mag_y, mag_z = s.mag()
        gyro_x, gyro_y, gyro_z = s.gyro()
        
        print('Gyroscope (radians/s): ({0:0.3f},  {1:0.3f},  {2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
        print('Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(accel_x, accel_y, accel_z))
        print('Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(mag_x, mag_y, mag_z))

        time.sleep(.1)

def mainj():
    s = sensor()

    while True:
        gyro = s.gyroj()
        print(gyro)

        time.sleep(.5)

if __name__ == '__main__':
    mainj()
