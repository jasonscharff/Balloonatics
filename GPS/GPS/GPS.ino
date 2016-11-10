#include <SoftwareSerial.h>
SoftwareSerial gpsSerial(10, 11);

void setup()
{
  Serial.begin(9600);
  gpsSerial.begin(9600);
}

void loop()
{
  if (gpsSerial.available())
  {
    Serial.write(gpsSerial.read());
  }
}
