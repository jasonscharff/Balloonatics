#include <ArduinoJson.h>

//Geiger
int geigerCounterPin = A3;
int geigerCount = 0;
double numGeigerCounts = 0;
double calibrationConstant = 0.49;
bool wasGeigerPreviouslyLow;

//Timing
long currentTime;
long prevTime;

//Transfer
int BAUD_RATE = 9600;

//Anemometer
bool wasAnemometerPreviouslyLow;
const int anemometerPin = 7;
int anemometerRPM = 0;

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(geigerCounterPin, INPUT);
  pinMode(anemometerPin, INPUT);
  currentTime = millis();
  prevTime = millis();
  wasGeigerPreviouslyLow = !analogRead(geigerCounterPin);
  wasAnemometerPreviouslyLow = !analogRead(anemometerPin);
}

void loop() {
  if (currentTime < 60000) {
    geigerCount = analogRead(geigerCounterPin);
    if (geigerCount == HIGH && wasGeigerPreviouslyLow == true) {
      wasGeigerPreviouslyLow = false;
      numGeigerCounts++;
    }
    else if (geigerCount == LOW) {
      wasGeigerPreviouslyLow = true;
    }
    int anemometer = analogRead(anemometerPin);
      if(anemometer == HIGH && wasAnemometerPreviouslyLow == true) {
      wasAnemometerPreviouslyLow = false;
      anemometerRPM++;
     } 
    else if(anemometer == LOW) {
      wasAnemometerPreviouslyLow = true;
    }
    
    currentTime = millis() - prevTime;
  } else {
    numGeigerCounts = numGeigerCounts * calibrationConstant;
    sendData(numGeigerCounts, anemometerRPM);

    numGeigerCounts = 0;
    currentTime = 0;
    prevTime = millis();
  }

}


void sendData(int geigerCount, int rpm) {
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["geiger_cpm"] = geigerCount;
  root["anemometer_rpm"] = rpm;
  char buffer[256];
  root.printTo(buffer, sizeof(buffer));
  Serial.println(buffer);
}


