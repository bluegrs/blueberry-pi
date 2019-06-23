/*
 * 
 * SUMMARY:
 * This script reads in configs from the Python "config.py" file, so that
 * the client and server are both using the same configurations.
 * 
 * TODO:
 * ~ Make static method to initialize configurations on game session startup
 */

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Configurations
{
    public static class Configs
    {
        public static string CONFIG_PATH; // Location of the configuration file

        // These are constants in the config file
        // wifi
        public static int WIFI_PORT = 5560;
        public static float TIMEOUT = 150;

        // nxp
        public static int PRECISION = 3;

        // client requests
        public static string ACCEL  = "0";
        public static string MAG    = "1";
        public static string GYRO   = "2";
        public static string EXIT   = "E";
        public static string KILL   = "K";

        // // Start is called before the first frame update
        // void Start()
        // {
        //     CONFIG_PATH = System.IO.Directory.GetCurrentDirectory() + @"\..\src\config.py";
        //     ImportConfigs();
        // }
        // 
        // void ImportConfigs()
        // {
        //     // Read each line of the file into a string array.
        //     string[] lines = System.IO.File.ReadAllLines(CONFIG_PATH);
        // 
        //     // Display the file contents by using a foreach loop.
        //     foreach (string line in lines)
        //     {
        // 
        //     }
        // }
    }
}
