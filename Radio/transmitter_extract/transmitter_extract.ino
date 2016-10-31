#include <SoftwareSerial.h>

String STARTER = "qNb4";
String ENDER = "j5st";

int BAUD_RATE_RASP = 9600;
int TRANSMITTER_SERIAL_BAUD = 4800;
SoftwareSerial transmitterSerial(0,1); 

void setup()
{
  Serial.begin(BAUD_RATE_RASP);
  while (!Serial) {
    //wait for usb serial
  }
  transmitterSerial.begin(TRANSMITTER_SERIAL_BAUD);
}

void loop()
{
  if (Serial.available()) {
    String s = Serial.read();
    if (s.length() > 0) {
      digitalWrite(3, HIGH);
      delay(10);
      s = STARTER + s + ENDER;
      transmitterSerial.print(s);
      delay(10);
      digitalWrite(3, LOW);
      delay(10);
    }

  }


}
