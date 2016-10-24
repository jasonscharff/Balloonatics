char dataString[50] = {0};
int a =0;

BAUD_RATE = 9600;


void setup() {
Serial.begin(BAUD_RATE);              //Starting serial communication
}

void loop() {
  a++;                          // a value increase every loop
  sprintf(dataString,"%02X",a); // convert a value to hexa
  Serial.println(dataString);   // send the data
  delay(1000);                  // give the loop some break
}
