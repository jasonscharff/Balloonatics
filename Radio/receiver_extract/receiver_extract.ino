#define INLENGTH 500
#define INTERMINATOR 13
char inString[INLENGTH+1];
int inCount;
String s;
String STARTER = "qNb4d5tR1q";
String ENDER = "j5st6w1rvU";
String NULL_TOKEN = "0000";

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
  s = extract(STARTER,ENDER,s);
  Serial.println(s);
}

String extract(String starter, String ender, String s)
{
  int startCount = 0;
  int endCount = 0;
  int startPos = 0;
  int endPos = 0;
  boolean inside = false;
  boolean ending = true;
  for (int i = 0; i < s.length(); i++)
  {
    if (!inside)
    {
      if (starter.charAt(startCount) == s.charAt(i))
      {
        startCount++;
      }
      else
      {
        startCount = 0;
      }
      if (startCount == starter.length())
      {
        inside = true;
        startPos = i + 1;
      }
    }
    else
    {
      if (ender.charAt(endCount) == s.charAt(i))
      {
        endCount++;
        ending = true;
      }
      else if (!(ender.charAt(endCount) == s.charAt(i)) and (ending == true))
      {
        endCount = 0;
        ending = false;
      }
      if (endCount == ender.length())
      {
        endPos = i - ender.length() + 1;
        i = s.length() + 1;
      }
    }
  }
  if (s.substring(startPos,endPos).length() < 2)
  {
    return s.substring(startPos,endPos);
  }
  else
  {
    return s.substring(startPos,endPos);
  }
}

