void setup()
{
  Serial.begin(9600);
  String s = "$GPGGA,175704.921,3727.2148,N,12211.4679,W,1,09,0.8,32.2,M,-32.1,M,,0000*58\n$GPGSA,A,3,21,20,26,13,15,05,25,16,18,,,,1.8,0.8,1.5*38\n$GPGSV,3,1,11,20,78,091,38,29,73,091,24,21,55,294,38,18,36,211,24*7B\n$GPGSV,3,2,11,26,31,301,37,25,27,192,27,15,26,126,39,05,25,046,31*78\n$GPGSV,3,3,11,13,20,091,25,16,12,323,27,02,00,078,*48\n$GPRMC,175704.921,A,3727.2148,N,12211.4679,W,000.0,314.8,311016,,,A*7F\n$GPVTG,314.8,T,,M,000.0,N,000.0,K,A*03";
  int gpgga = s.indexOf("$GPGGA");
  s = s.substring(gpgga);
  Serial.println(getTime(s));
  Serial.println(getLat(s));
  Serial.println(getLon(s));
  Serial.println(getAlt(s));
}

void loop() {

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

