#include <ArduinoJson.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>

const int BAUD_RATE = 9600;

//range finder
const int pwPin = 7;
double pulse, inches, cm;
long time;

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

void setup()
{
  Serial.begin(BAUD_RATE);
  Serial.println(F("BME280 test"));

  if (!bme.begin()) {   
     Serial.println("Could not find a valid BME280 sensor, check wiring!");
     while (1);
  }
  
  pinMode(cutoffPin, OUTPUT);
}

void loop()
{
  //range finder data collection
  pinMode(pwPin, INPUT);
  pulse = pulseIn(pwPin, HIGH);
  time = pulseIn(pwPin, HIGH);
  inches = pulse/147.0;
  cm = inches*2.54;

  Serial.print(inches);
  Serial.print("in, ");
  Serial.print(cm);
  Serial.print("cm, ");
  Serial.print("Time:");
  Serial.print(time);
  Serial.println();

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
