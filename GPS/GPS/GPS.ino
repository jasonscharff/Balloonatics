#include <SoftwareSerial.h>
SoftwareSerial gpsSerial(10, 11);
String content = "";

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
/*
    int gpgga = s.indexOf("$GPGGA");
    s = s.substring(gpgga);
    Serial.write(getTime(s));
    Serial.write(getLat(s));
    Serial.write(getLon(s));
    Serial.write(getAlt(s));
  }
}

String getTime(String s)
{
  int nextComma = s.indexOf(',');
  s = s.substring(nextComma + 1);
  nextComma = s.indexOf(',');
  String t = s.substring(0, nextComma);
  t = "Time: " + t.substring(0, 2) + ":" + t.substring(2, 4) + ":" + t.substring(4);
  return t;
}

String getLat(String s)
{
  int nextComma = s.indexOf(',');
  s = s.substring(nextComma + 1);
  nextComma = s.indexOf(',');
  String lat = "Lat: " + s.substring(0, nextComma);
  nextComma = s.indexOf(',');
  s = s.substring(nextComma + 1);
  lat = lat + s.charAt(0);
  return lat;
}

String getLon(String s)
{
  int nextComma = s.indexOf(',');
  s = s.substring(nextComma + 1);
  nextComma = s.indexOf(',');
  String lon = "Lon: " + s.substring(0, nextComma);
  s = s.substring(nextComma + 1);
  lon = lon + s.charAt(0);
  return lon;
}

String getAlt(String s)
{
  int nextComma;
  for (int i = 0; i < 4; i++)
  {
    nextComma = s.indexOf(',');
    s = s.substring(nextComma + 1);
  }
  nextComma = s.indexOf(',');
  String alt = "Alt: " + s.substring(0, nextComma);
  s = s.substring(nextComma + 1);
  alt = alt + s.charAt(0);
  return alt;
}
*/
