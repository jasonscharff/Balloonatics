/*
    File name: pressure_rangefinder_cutoff.ino
    Authors: Niky Arora, Aaron Lee, Zack Hurwitz, and Jason Scharff
    Arduino Version: 1.6.9
    Description: This file provides the code for one of the three arduinos 
    connected to the Raspberry Pi. In particular, this file manages the collection of:
    1. Exterior Pressure
    2. Exterior Humidity
    3. Exterior Temperature
    4. Estimated Altitude
    5. Aaron Lee Experiment on Voltage from Solar Panels surrounded by different colored films.
    6. Niky Arora Experiment on Speed of Sound.

    Exterior pressure, exterior humidity, exterior temperature,and estimated altitude are 
    all collected using an Adafruit BME280 sensor

    In addition, this file also handles the cutdown mechanism by triggering a relay to
    discharge capacitors when a certain signal is received from the Raspberry Pi.
*/

//Import the Adafruit BME280 library.
#include <Adafruit_BME280.h>

//Import library to allow interfacing with SPI––a dependency of Adafruit's BME280 library
#include <SPI.h>
//Import standard Adafruit Sensor library––a dependency of Adafruit's BME280 library.
#include <Adafruit_Sensor.h>

//Import the Arduino JSON library to be able to send data to raspberry pi in JSON format.
#include <ArduinoJson.h>

//Standard baud rate at which to send data to the raspberry pi over.
const int BAUD_RATE = 9600;

//range finder

//Pin of the proximity sensor
const int pwPin = 7;
//Variable to store pulse.
long rangeFinderTime;

//BME 280 pressure sensor pin-outs

//Pin for SPI clock.
#define BME_SCK 13
//Pin SPI for Master Input, Slave Output
#define BME_MISO 12
//Pin for SPI Master Output, Slave Input.
#define BME_MOSI 11
//Pin for SPI Slave Select
#define BME_CS 10

//Create a macro for the sea level pressure to use
//for BME280 approximation of altitude in hectopascals.
#define SEALEVELPRESSURE_HPA (1013.25)

//Initialize the BME280 object over SPI.
Adafruit_BME280 bme(BME_CS);

//pin to trigger cutoff mechanism by switching a relay.
int cutoffPin = A1;

//Pin for the solar panel surrounded by a blue film.
int blue = A2;
//Pin for the solar panel surrounded by a white film.
int white = A3;
//Pin for a solar panel surrounded by a red film.
int red = A4;
//Variable to store voltage from the blue solar panel.
int blueVoltage = 0;
//Variable to store voltage from the white solar panel.
int whiteVoltage = 0;
//Variable to storage voltage from the red solar panel.
int redVoltage = 0;

//Signal sent by Raspberry Pi to trigger cutoff.
char CUTOFF_SIGNAL = 'c';


//Function called by Arduino, exactly once upon boot.
//Used for initial configuration.
void setup() {
  //Turn on the serial communication with the raspberry pi at the standard BAUD_RATE.
  Serial.begin(BAUD_RATE);
  //Turn on the Adafruit BME280 combined pressure/humidity/temperature sensor.
  bme.begin();
  //Set the pin for the relay to trigger the cutoff as output.
  pinMode(cutoffPin, OUTPUT);
  //Set the pin to read the time taken for sound to travel across a fixed distance in the payload to input.
  pinMode(pwPin, INPUT);
}

//Function called by Arduino repeatedly.
void loop() {

  //Detect if the Raspberry Pi has sent a signal to trigger cutdown.
  detectSignal();
  //Read time taken for sound to travel fixed distance in the payload in seconds.
  rangeFinderTime = pulseIn(pwPin, HIGH);

  //bme280
  //Read temperature in degrees Celsius from BME280.
  double temperature = bme.readTemperature();
  //Read pressure in pascals from BME280.
  double pressure = bme.readPressure();
  //Read altitude as estimated by the BME280 sensor with the sea
  //level pressure of SEALEVELPRESSURE_HPA (in hectopascals).
  //Not actually used, but an interesting data point nonetheless.
  double bme_altitude = bme.readAltitude(SEALEVELPRESSURE_HPA);
  //Read humidity from BME280 as a relative percentage.
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

//Function to detect if the raspberry pi has
//sent the cutdown signal and, if so, trigger cutdown.
void detectSignal() {
  //Read in any input from raspberry pi.
  char piInput = Serial.read();
  //Check if the input is equal to the cutoff signal.
  if (piInput == CUTOFF_SIGNAL) {
    //If the input is equal to the cutoff signal, trigger cutdown.
    cutoff();
  }
}

//Function to send data from sensors to the raspberry pi over JSON.
void sendFrequentData(double temperature, double pressure, double bme_altitude, double humidity, double rangeFinderTime, int blue, int white, int red) {
    //Allocate space for the JSON object in memory.
    StaticJsonBuffer<200> jsonBuffer;
    //Create a JSON object in the allocated memory.
    JsonObject& root = jsonBuffer.createObject();
    //Add the exterior temperature to the JSON object.
    root["exterior_temperature"] = temperature;
    //Add the exterior humidity to the JSON object.
    root["exterior_humidity"] = humidity;
    //Add the exterior pressure to the JSON object. Include 5 decimal places.
    root["exterior_pressure"] = double_with_n_digits(pressure, 5);
    //Add the altitude as estimated by the BME280 sensor. Not used in the data, but an interesting data point, nonetheless.
    root["estimated_altitude"] = bme_altitude;
    //Add the time taken for the sound to travel across the fixed distance in the payload to the JSON object.
    root["sound_time"] = rangeFinderTime;
    //Add the voltage read from the solar panel surrounded by a white film to the JSON object.
    root["white_voltage"] = white;
    //Add the voltage read from the solar panel surrounded by a red film to the JSOn object
    root["red_voltage"] = red;
    //Add the voltage read from the solar panel surrounded by a blue film to the JSON object
    root["blue_voltage"] = blue;
    //Allocate a character buffer in memory to store the JSON object as a string (an array of characters) in memory.
    char buffer[256];
    //Convert the JSON object into a string in the memory location of the character buffer created above.
    root.printTo(buffer, sizeof(buffer));
    //Send JSON string over serial to the Raspberry Pi.
    Serial.println(buffer);
}

//Function to begin the cutdown process.
void cutoff() {
  //Turn relay in the on position to trigger the capacitors to discharge.
  analogWrite(cutoffPin, 255);
  //Wait 1 second to ensure ample time for the relay to have switched
  //triggering the capacitors.
  delay(1000);
  //Switch back the relay to the off position.
  analogWrite(cutoffPin, 0);
}
