String STARTER = "qNb4d5tR1q";
String ENDER = "j5st6w1rvU";
int BAUD_RATE = 4800;
String toSend = "";
char queued = 0;

void setup()
{
  Serial.begin(BAUD_RATE);
  Serial1.begin(BAUD_RATE);
}

void loop()
{
//    for (int i = 0; i < 167; i++)
//    {
      digitalWrite(3,HIGH);
      long currentTime = millis();
      while (millis()-currentTime < 10) {
        if (queued <= 0) {
          char c = Serial.read();
          if(c>0) {
          queued = c;
        }
        }
      }
      
      if (queued > 0) {
        Serial1.print(STARTER);
        Serial1.print(String(queued) + "ello");
        Serial1.print(ENDER);
      }
      queued = 0;
  
    
      currentTime = millis();
      while (millis() - currentTime < 10) {
         if (queued <= 0) {
          char c = Serial.read();
          if(c>0) {
          queued = c;
        }
        }
      }
      digitalWrite(3,LOW);
      while (millis() - currentTime < 10) {
         if (queued <= 0) {
          char c = Serial.read();
          if(c>0) {
          queued = c;
        }
        }
      }

//      char s = Serial.read();
//      if (s > 0)
//      {
//        toSend += String(s);
//        digitalWrite(12,HIGH);
//      }
//      else
//      {
//        Serial.print(STARTER + toSend + ENDER);
//        toSend = "";
//        digitalWrite(12,LOW);
//      }
//      delay(10);
//      digitalWrite(3,LOW);
//      delay(10);
//    }
//    delay(5000);
}
