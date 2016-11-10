#include <ArduinoJson.h>

int pressure = A0;
int pressvalue = 0;

const int BAUD_RATE = 9600;

void setup() {
  Serial.begin(BAUD_RATE);
  analogReference(EXTERNAL);
}

void loop() {
  int rawPressureValue = analogRead(pressure);
  sendRawPressure(rawPressureValue);
}

void sendRawPressure(int rawPressure) {
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["raw_exterior_pressure"] = rawPressure;
  root.printTo(Serial);
}

