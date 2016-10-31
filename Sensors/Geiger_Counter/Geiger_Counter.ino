int geigerCounterPin = A0;
int geigerCount = 0;
long time;
int numCounts = 0;
int cpm;

void setup() 
{
  Serial.begin(9600);
  pinMode(geigerCounterPin, INPUT);
}

void loop() 
{
  geigerCount = analogRead(geigerCounterPin);
  if(geigerCount == HIGH)
  {
    numCounts = numCounts + 1;
    delay(10);
  }
  time = millis();
  if(time % 60000 == 0)
  {
    Serial.println(numCounts);
    numCounts = 0;
    delay(10);
  }
}


