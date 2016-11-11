int pin = A1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(pin, 255);
  //delay(1000);
  //analogWrite(pin, 0);
  //delay(1000);
}
