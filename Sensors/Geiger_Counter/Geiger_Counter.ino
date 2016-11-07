int geigerCounterPin = A3;
int geigerCount = 0;
long currentTime;
long prevTime;
int numCounts = 0;
int calibate = 0.49;
bool wasPreviouslyLow;

void setup() 
{
  Serial.begin(9600);
  pinMode(geigerCounterPin, INPUT);
  currentTime = millis();
  prevTime = millis();
  wasPreviouslyLow = !analogRead(geigerCounterPin);
}

void loop() 
{
  while(currentTime < 60000)
  {
    geigerCount = analogRead(geigerCounterPin);
    if(geigerCount == HIGH && wasPreviouslyLow == true)
    {
      wasPreviouslyLow = false;
      numCounts++;
    } 
    else if(geigerCount == LOW)
    {
      wasPreviouslyLow = true;
    }
    currentTime = millis() - prevTime;
  }
  numCounts = numCounts*calibrate;
  Serial.println(numCounts);
  numCounts = 0;
  currentTime = 0;
  prevTime = millis();
}
