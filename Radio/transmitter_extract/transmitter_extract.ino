String STARTER = "qNb4";
String ENDER = "j5st";

int BAUD_RATE = 9600;

void setup()
{
  Serial.begin(BAUD_RATE);
}

void loop()
{
  if (Serial.available()) {
    String x = Serial.read();
    if (x != null && x.length() > 0) {
      digitalWrite(3, HIGH);
      delay(10);
      String s = "Hello";
      s = STARTER + s + ENDER;
      Serial.print(s);
      delay(10);
      digitalWrite(3, LOW);
      delay(10);
    }

  }


}
