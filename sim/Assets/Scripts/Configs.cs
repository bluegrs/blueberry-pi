/*
 * 
 * SUMMARY:
 * This script reads in configs from the Python "config.py" file, so that
 * the client and server are both using the same configurations.
 * 
 */

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Configs : MonoBehaviour
{
    string CONFIG_PATH; // Location of the configuration file

    // These are constants in the config file
    // wifi
    int WIFI_PORT;
    float TIMEOUT;

    // nxp
    int PRECISION;

    // client requests
    string ACCEL;
    string MAG;
    string GYRO;
    string EXIT;
    string KILL;

    // Start is called before the first frame update
    void Start()
    {
        CONFIG_PATH = System.IO.Directory.GetCurrentDirectory() + @"\..\src\config.py";
        ImportConfigs();
    }

    void ImportConfigs()
    {
        // Read each line of the file into a string array.
        string[] lines = System.IO.File.ReadAllLines(CONFIG_PATH);

        // Display the file contents by using a foreach loop.
        foreach (string line in lines)
        {

        }
    }
}
