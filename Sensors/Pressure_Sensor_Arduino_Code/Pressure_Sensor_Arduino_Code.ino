/*
   Blink based on temperature
*/
 
// Pin 13 has an LED connected on most Arduino boards.

const int led = 13;
int pressure = A0;
int pressvalue = 0;
int time =0;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT); 
  Serial.begin(9600);
  analogReference(EXTERNAL);
}

// the loop routine runs over and over again forever:
void loop() {
 digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(500);               // wait for a half second
  pressvalue = analogRead(pressure);
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  delay(500);               // wait for a half second
  time = time + 1;
  Serial.print("time = ");
  Serial.print(time);
  Serial.print("    Pressure = ");
  Serial.println(pressvalue);
 
}
