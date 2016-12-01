/*
    File name: Geiger_Counter.ino
    Authors: Tfom Welch, Hayden Pegley, and Jason Scharff
    Arduino Version: 1.6.9
    Description: This file provides the code for one of the three arduinos 
    connected to the Raspberry Pi. In particular, this file manages the collection of:
    1. Geiger Counter Counts Per Minute
    2. Anemometer Spins Per Minute.

   Both the gieger counter and anemometer code are very similar
   as they just collect the number of high voltages recorded during
   a one minute period. As such, data is sent once per minute to the raspberry pi.

   All data is then sent to the Raspberry Pi over JSON.
*/

//Import the Arduino JSON library to be able to send data to raspberry pi in JSON format.
#include <ArduinoJson.h>

//Geiger

//Pin of the geiger counter.
int geigerCounterPin = A3;
//Variable to store high/low reading from the geiger counter.
int geigerCount = 0;
//Variable to store number of total geiger counts
//in the last minute. 
double numGeigerCounts = 0;
//To avoid double counting two high voltage reads
//we want to only count times in which the voltage reading has changed.
bool wasGeigerPreviouslyLow;

//Timing
//Variable to store the time elapsed since the beginning of
//previous one minute reading period.
long currentTime;
//Variable to store the time at the beginning of the 
//beginning of the last one minute reading period.
long prevTime;

//Standard baud rate at which to send data to the raspberry pi over.
int BAUD_RATE = 9600;

//Anemometer
//To avoid double counting two high voltage reads
//we want to only count times in which the voltage reading has changed.
bool wasAnemometerPreviouslyLow;
//Pin of a hall chip which is triggered each time a
//magnet on the anemometer passes by which happens one time per rotation.
const int anemometerPin = 7;
//Variable to store number of total spins in the last minute.
int anemometerRPM = 0;

//Function called by Arduino, exactly once upon boot.
//Used for initial configuration.
void setup() {
   //Turn on the serial communication with the raspberry pi at the standard BAUD_RATE.
  Serial.begin(BAUD_RATE);
  //Configure the geiger counter pin as an input.
  pinMode(geigerCounterPin, INPUT);
  //Configure the anemometer pin as an input.
  pinMode(anemometerPin, INPUT);
  //set the current time variable to the current time in millis.
  currentTime = millis();
  //Set the previous time variable to 
  prevTime = millis();
  //Set the variable was geiger previously low based
  //off of the current geiger reading.
  wasGeigerPreviouslyLow = !analogRead(geigerCounterPin);
   //Set the variable was anemometer previously low based
  //off of the current anemometer reading.
  wasAnemometerPreviouslyLow = !analogRead(anemometerPin);
}

void loop() {
  //Check if the one minute reading period has finished.
  if (currentTime < 60000) {
    //In one minute reading period.

    //Determine if the geiger counter is currently reporting high or low.
    geigerCount = analogRead(geigerCounterPin);
    //If the geiger counter is reading high and it was previously low
    //i.e a change has been detected
    if (geigerCount == HIGH && wasGeigerPreviouslyLow == true) {
      //Set was previously low to false as it is currently high.
      wasGeigerPreviouslyLow = false;
      //Increase the number of geiger counts seen in the last minute by 1.
      numGeigerCounts++;
    }
    //If the geiger counter is low.
    else if (geigerCount == LOW) {
      //Change wasPreviouslyLow to true as it is currently low.
      wasGeigerPreviouslyLow = true;
    }
    //Check if the anemometer pin (a hall chip) is currently reading high or low..
    int anemometer = analogRead(anemometerPin);
    //If the anemometer is currently high and the anemometer was previously low
    //i.e a change has been detected
     if(anemometer == HIGH && wasAnemometerPreviouslyLow == true) {
      //Set was previously low to false as it is currently high.
      wasAnemometerPreviouslyLow = false;
      //Increase the anemometer rpm by 1.
      anemometerRPM++;
     } 
      //If the anemometer pin is reading low.
    else if(anemometer == LOW) {
      //Change wasPreviouslyLow to true as it is currently low.
      wasAnemometerPreviouslyLow = true;
    }
    //Reset current time to the time elapsed since previous time.
    currentTime = millis() - prevTime;
  } else { //A minute has elapsed since the previous data collection period began.
    //Send anemometer and geiger counter data to raspberry pi.
    sendData(numGeigerCounts, anemometerRPM);
    //Reset the geiger count to 0
    numGeigerCounts = 0;
    //During the launch the anemometer was not reset when it should have
    //This is discussed in the paper, but the data was fully recoverable.

    
    //Reset the time elapsed since the last 1 minute data collecting period
    //to zero to prepare for new data collecting period.
    currentTime = 0;
    //Reset the time the data collection period began to the current time.
    prevTime = millis();
  }

}

//Function to send geiger counter data and anemometer data over JSON to raspberry pi.
void sendData(int geigerCount, int rpm) {
  //Allocate space for the JSON object in memory.
  StaticJsonBuffer<200> jsonBuffer;
  //Create a JSON object in the allocated memory.
  JsonObject& root = jsonBuffer.createObject();
  //Add the geiger counter data to the JSON object.
  root["geiger_cpm"] = geigerCount;
  //Add the anemometer rpm to the JSON object.
  root["anemometer_rpm"] = rpm;
  //Allocate a character buffer in memory to store the JSON object as a string (an array of characters) in memory.
  char buffer[256];
   //Convert the JSON object into a string in the memory location of the character buffer created above.
  root.printTo(buffer, sizeof(buffer));
  //Send JSON string over serial to the Raspberry Pi.
  Serial.println(buffer);
}


