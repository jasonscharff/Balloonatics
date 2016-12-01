/*
    File name: GPS.ino
    Authors: Aaron Lee and Jason Scharff
    Arduino Version: 1.6.9
    Description: This file provides the code for one of the three arduinos 
    connected to the Raspberry Pi. In particular, this file manages the collection of
    GPS data. Because aquiring GPS signal is a long running process that take take
    greater than half a second, the GPS is relegated to a seperate Arduino
    to not interfere with other sensors.

    The GPS Module used is a Sparkfun Venus and all readings
    are sent directly to the Raspberry Pi for proceesing.

    There is no processing of data on the Arduino.
*/

//Import SoftwareSerial library to read GPS data over
//software serial as the hardware serial is used
//to communicate with the Raspberry Pi.
#include <SoftwareSerial.h>
//Initialize the GPS object using RX pin 10 and TX pin 11.
SoftwareSerial gpsSerial(10, 11);

//Standard baud rate at which to send data to the raspberry pi over and read from GPS over.
const int BAUD_RATE = 9600;

//Function called by Arduino, exactly once upon boot.
//Used for initial configuration.
void setup()
{
  //Turn on the serial communication with the raspberry pi at the standard BAUD_RATE.
  Serial.begin(BAUD_RATE);
  //Turn on the serial communication with the GPS at the standard BAUD_RATE.
  gpsSerial.begin(BAUD_RATE);
}

//Function called by Arduino repeatedly.
void loop()
{
  //Check if gpsSerial is available before attempting to read from it.
  if (gpsSerial.available())
  {
    //Read data from GPS and immediately send it to the raspberry
    //pi for processing and storage.
    //Arduino string libraries are known to leak memory and thus all
    //string processing is done on the Raspberry Pi.
    Serial.write(gpsSerial.read());
  }
}
