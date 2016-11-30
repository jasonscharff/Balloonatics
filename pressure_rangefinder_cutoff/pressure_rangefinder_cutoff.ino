//Import the Adafruit BME280 library.
#include <Adafruit_BME280.h>

//Import library to allow interfacing with SPI––a dependency of Adafruit's BME280 library
#include <SPI.h>
//Import standard Adafruit Sensor library––a dependency of Adafruit's BME280 library.
#include <Adafruit_Sensor.h>

//Import the Arduino JSON library to be able to send data to raspberry pi in JSON format.
#include <ArduinoJson.h>



const int BAUD_RATE = 9600;

//range finder
const int pwPin = 7;
double pulse;
long rangeFinderTime;
double CM_TIME = 57.874;

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


char CUTOFF_SIGNAL = 'c';



void setup() {
  Serial.begin(BAUD_RATE);
  bme.begin();
  pinMode(cutoffPin, OUTPUT);
  pinMode(pwPin, INPUT);
}

void loop() {

  detectSignal();
  //range finder data collection
  pulse = pulseIn(pwPin, HIGH);
  rangeFinderTime = pulseIn(pwPin, HIGH);
  double cm = pulse/CM_TIME;

  //bme280
  double temperature = bme.readTemperature();
  double pressure = bme.readPressure();
  double bme_altitude = bme.readAltitude(SEALEVELPRESSURE_HPA);
  double humidity = bme.readHumidity();

  int blueVoltage = analogRead(blue); // stores voltage read in from blue solar panel
  int whiteVoltage = analogRead(white); // stores voltage read in from white solar panel
  int redVoltage = analogRead(red);
  
  sendFrequentData(temperature,pressure,bme_altitude, humidity,rangeFinderTime, blueVoltage, whiteVoltage,redVoltage);

   long current_time = millis();
    //wait one second
    while (millis() - current_time < 1000) {
      detectSignal();
    }
}

void detectSignal() {
  char piInput = Serial.read();
  if (piInput == 'c') {
    cutoff();
  }
}

void sendFrequentData(double temperature, double pressure, double bme_altitude, double humidity, double rangeFinderTime, int blue, int white, int red) {
    StaticJsonBuffer<200> jsonBuffer;
    JsonObject& root = jsonBuffer.createObject();
    root["exterior_temperature"] = temperature;
    root["exterior_humidity"] = humidity;
    root["exterior_pressure"] = double_with_n_digits(pressure, 5);
    root["estimated_altitude"] = bme_altitude;
    root["sound_time"] = rangeFinderTime;
    root["white_voltage"] = white;
    root["red_voltage"] = red;
    root["blue_voltage"] = blue;
    char buffer[256];
    root.printTo(buffer, sizeof(buffer));
    Serial.println(buffer);
}

void cutoff() {
  analogWrite(cutoffPin, 255);
  delay(1000);
  analogWrite(cutoffPin, 0);
}
