#define INLENGTH 500
char inString[INLENGTH+1];
int inCount;
String s;

void setup()
{
  Serial.begin(4800);
}

void loop()
{
  Serial.flush();
  delay(1);
  inCount = 0;
  do
  {
    while (!Serial.available());
    inString[inCount] = Serial.read();
  } while (++inCount < INLENGTH);
  inString[inCount] = 0;
  s = String(inString);
  Serial.println(s);
}
