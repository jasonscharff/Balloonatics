#include <ArduinoJson.h>

//The analog pin to trigger the cutdown mechanism
int cutoffPin = A1;
//The standard baud rate used to communicate with the raspberry pi.
int BAUD_RATE = 9600;

//Setup function: called exactly once on bootup
void setup() {
  //Begin the serial communication with the raspberry pi.
  Serial.begin(BAUD_RATE);
  //configure the cutoff pin as output––arduino sends voltage through it.
  pinMode(cutoffPin, OUTPUT);
}

//Loop function: called continuously
void loop() {
  String raspberryPiInput = Serial.readString();
  if (raspberryPiInput.length() > 0) {
      StaticJsonBuffer<200> jsonBuffer;
      JsonObject& root = jsonBuffer.parseObject(raspberryPiInput);
      boolean shouldCut = root["altitudeReached"];
      if(shouldCut) {
        cutoff();
      }
  }
  
}

//Function to trigger the cutoff mechanism.
void cutoff() {
  //Send full signa
  analogWrite(cutoffPin, 255);
}

