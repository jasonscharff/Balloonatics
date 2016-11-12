#include <ArduinoJson.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>

const int BAUD_RATE = 9600;

//range finder
const int pwPin = 7;
double pulse, inches, cm;
long time;

double INCHES_TO_CM_CONVERSION_FACTOR = 2.54;

//pressure sensor
#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)




//Adafruit_BME280 bme; // I2C
Adafruit_BME280 bme(BME_CS); // hardware SPI
//Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO,  BME_SCK);

//cutoff
int cutoffPin = A1;

//aaron individual
int blue = A2;
int white = A3;
int red = A4;
int blueVoltage = 0;
int whiteVoltage = 0;
int redVoltage = 0;



void setup() {
  Serial.begin(BAUD_RATE);
  bme.begin();
  pinMode(cutoffPin, OUTPUT);
  pinMode(pwPin, INPUT);
}

void loop() {
  //range finder data collection
  pulse = pulseIn(pwPin, HIGH);
  time = pulseIn(pwPin, HIGH);
  inches = pulse/147.0;
  cm = inches*INCHES_TO_CM_CONVERSION_FACTOR;

  Serial.print(inches);
  Serial.print(cm);

  //collect pressure, temperature, humidity sensor values
  Serial.print("T = ");
  Serial.println(bme.readTemperature());

  Serial.print("P = ");
  Serial.println(bme.readPressure() / 100.0F);

  Serial.print("Approx. Altitude = ");
  Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
  Serial.println(" m");

  Serial.print("Humidity = ");
  Serial.print(bme.readHumidity());
  Serial.println(" %");

  Serial.println();

  //send a signal to relay to trigger cutoff
  String raspberryPiInput = Serial.readString();
  if (raspberryPiInput.length() > 0) {
      StaticJsonBuffer<200> jsonBuffer;
      JsonObject& root = jsonBuffer.parseObject(raspberryPiInput);
      boolean shouldCut = root["altitudeReached"];
      if(shouldCut) {
        cutoff();
      }
  }
  
  delay(1000);
}

void cutoff() {
  analogWrite(cutoffPin, 255);
}
