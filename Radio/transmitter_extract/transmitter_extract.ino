String STARTER = "qNb4";
String ENDER = "j5st";

void setup()
{
  Serial.begin(4800);
}

void loop()
{
  digitalWrite(3,HIGH);
  delay(10);
  String s = "Hello";
  s = STARTER + s + ENDER;
  Serial.print(s);
  delay(10);
  digitalWrite(3,LOW);
  delay(10);
}
