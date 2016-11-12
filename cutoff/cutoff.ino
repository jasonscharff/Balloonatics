#include <ArduinoJson.h>


int cutoffPin = A1;
int BAUD_RATE = 9600;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE);
  pinMode(cutoffPin, OUTPUT);
}

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

void cutoff() {
  analogWrite(cutoffPin, 255);
}

