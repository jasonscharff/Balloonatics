#include <ArduinoJson.h>

int geigerCounterPin = A3;
int geigerCount = 0;
long currentTime;
long prevTime;
double numCounts = 0;
double calibrationConstant = 0.49;
bool wasPreviouslyLow;
int BAUD_RATE = 9600;

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(geigerCounterPin, INPUT);
  currentTime = millis();
  prevTime = millis();
  wasPreviouslyLow = !analogRead(geigerCounterPin);
}

void loop() {
  while (currentTime < 60000) {
    geigerCount = analogRead(geigerCounterPin);
    if (geigerCount == HIGH && wasPreviouslyLow == true) {
      wasPreviouslyLow = false;
      numCounts++;
    }
    else if (geigerCount == LOW) {
      wasPreviouslyLow = true;
    }
    currentTime = millis() - prevTime;
  }
  numCounts = numCounts * calibrationConstant;
  sendNumCounts(numCounts);

  numCounts = 0;
  currentTime = 0;
  prevTime = millis();
}


void sendNumCounts(int numCounts) {
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["geiger_cpm"] = String(numCounts);
  char buffer[256];
  root.printTo(buffer, sizeof(buffer));
  Serial.println(buffer);
}


