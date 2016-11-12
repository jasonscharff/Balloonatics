int blue = A0;
int white = A1;
int red = A2;
int blueVoltage = 0;
int whiteVoltage = 0;
int redVoltage = 0;
int BAUD_RATE = 9600;

void setup()
{
  Serial.begin(BAUD_RATE);
}

void loop()
{
  blueVoltage = analogRead(blue); // stores voltage read in from blue solar panel
  whiteVoltage = analogRead(white); // stores voltage read in from white solar panel
  redVoltage = analogRead(red); // stores voltage read in from red solar panel
  Serial.println("Blue, " + String(blueVoltage));
  Serial.println("White, " + String(whiteVoltage));
  Serial.println("Red, " + String(redVoltage));
  delay(5000); // delay for the loop, can be adjusted to whatever you see fit for data collection
}
