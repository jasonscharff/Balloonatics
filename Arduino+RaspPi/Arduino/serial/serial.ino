int BAUD_RATE = 9600;


void setup() {
Serial.begin(BAUD_RATE);              //Starting serial communication
}

void loop() {
Serial.println("Hello Pi");
delay(2000);
}
