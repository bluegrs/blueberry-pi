/*
 * 
 * SUMMARY --------------------------------------------------------------------------------------------
 * 
 * This class is designed to directly receive data from the RasPi through the socket connection instead
 * of communicating to the local Python scripts (drivers.py). This reduces controller latency in the 
 * simulation and add to the system's portability because it requires fewer third party tools.
 * 
 * UPDATES --------------------------------------------------------------------------------------------
 * 
 * 6/15/2019:   Created basic TCP socket class following a guide posted by "danielbierwirth" on GitHub.
 * 
 * 6/18/2019:   Script searches for LAN connection on configured port. Cleanup functions allow the server 
 *              to continue operating instead of crashing.
 * 
 * TODO -----------------------------------------------------------------------------------------------
 *  
 *  ~ Assign port number through the configuration script.
 *  
 *  ~ Write to a resource instead of a local variable.
 */

using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class SocketResource : MonoBehaviour
{
    private TcpClient socketConnection;
    private Thread clientReceiveThread;

    private string serverIP;
    int port;

    // Use this for initialization 	
    void Start()
    {
        // variable initializations
        serverIP = "192.168.1.";
        port = 5560;

        FindServerIP();         // before making a connection to the server, find its IP.
        ConnectToTcpServer();   // make a socket connection to the server.
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Send("0");
        }
    }

    /*
     *  SUMMARY:
     *  Set up a socket connection to the server. Searches through IP addresses on 
     *  the configured port automatically until a connection is found.
     */
    private void ConnectToTcpServer()
    {
        try
        {
            clientReceiveThread = new Thread(new ThreadStart(ListenForData));
            clientReceiveThread.IsBackground = true;
            clientReceiveThread.Start();
        }
        catch (Exception e)
        {
            Debug.Log("On client connect exception " + e);
        }
    }

    /*
     * SUMMARY: Search for the correct server IP and assign it to the global.
     */
     private void FindServerIP()
     {
        // Test all local area network (LAN) IPs
        for (int ping = 0; ping < 255; ping++)
        {
            string pingIP = serverIP + ping.ToString();
            Debug.Log("Pinging: " + pingIP);

            try
            {
                // Try connecting to the IP with a timeout of .05 seconds
                socketConnection = new TcpClient();
                if (!socketConnection.ConnectAsync(pingIP, port).Wait(100))
                {
                    continue; // Connection failure
                }

                // allows reconnection for synchronous in ListenForData
                Send("E");
                socketConnection.GetStream().Close();
                socketConnection.Close();
                serverIP = pingIP;
                break;
            }
            catch
            {
                Debug.Log("Connection Failure");
            }
        }
     }

    /*
     *  SUMMARY:
     *  Background thread for catching messages from the server.
     */
    private void ListenForData()
    {
        try
        {
            // Tries to create a synchronous tcp socket
            socketConnection = new TcpClient(serverIP, 5560);
            Byte[] bytes = new Byte[1024];
            while (true)
            {
                // Get a stream object for reading 				
                using (NetworkStream stream = socketConnection.GetStream())
                {
                    int length;

                    // Read incomming stream into byte arrary. 					
                    while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                    {
                        var incommingData = new byte[length];
                        Array.Copy(bytes, 0, incommingData, 0, length);

                        // Convert byte array to string message. 						
                        // string serverMessage = Encoding.ASCII.GetString(incommingData);
                        string serverMessage = Encoding.UTF8.GetString(incommingData);
                        Debug.Log("server message received as: " + serverMessage);
                    }
                }
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }

    /*
     * SUMMARY:
     * Send request to server over the socket connection established with ConnectToTcpServer
     */
    private void Send(string clientRequest)
    {
        if (socketConnection == null)
        {
            return;
        }
        try
        {
            // Get a stream object for writing. 			
            NetworkStream stream = socketConnection.GetStream();
            if (stream.CanWrite)
            {
                // Convert string message to byte array.    
                // byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(clientMessage);
                byte[] clientMessageAsByteArray = Encoding.UTF8.GetBytes(clientRequest);

                // Write byte array to socketConnection stream.                 
                stream.Write(clientMessageAsByteArray, 0, clientMessageAsByteArray.Length);
                Debug.Log("Client sent his message - should be received by server");
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }

    /*
     * SUMMARY:
     * Send request to server to end the socket connection. The client requests to disconnect
     * from the server.
     */
    void OnApplicationQuit()
    {
        Debug.Log("Application ending after " + Time.time + " seconds");

        // EXIT signals server that the connection socket should be closed.
        try
        {
            Send("E");
        }
        catch
        {
            Debug.Log("No connection available.");
        }

        // Stop the listener thread so that it's not trying
        // to receive data from the server when the connection
        // socket is closed.
        clientReceiveThread.Abort();

        // Clean close the socket on client side.
        try
        {
            socketConnection.GetStream().Close();   // close stream
            socketConnection.Close();               // close connection
        }
        catch
        {
            Debug.Log("No connection available.");
        }
    }
}