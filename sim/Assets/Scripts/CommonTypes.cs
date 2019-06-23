using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Common
{ 
    /*
     *  SUMMARY:
     *  Use this for accessing the specific queue's data in the 2D array of sensor data queues.
     *  
     *  EXAMPLE USAGE:
     *  float test = sensorData[Sensor.ACCEL, SENSOR.X].Dequeue();   // for reading
     *  sensorData[Sensor.GYRO, Sensor.Y].Enqueue(2.53);             // for writing
     */
    public enum Sensors
    {
        // For selecting the sensor array to access
        ACCEL = 0,
        GYRO = 1,
        MAG = 2,
    
        // For selecting the queue to read+write in the sensor array
        X = 0,
        Y = 1,
        Z = 2
    }
}
