const int analogOutPin = 5;
// Analog output pin that the LED is attached to
const int reset = 4;
    
int outputValue = 0;        // value output to the PWM (analog out)

void setup() {
  pinMode(reset,INPUT);
  analogWrite(analogOutPin, 3);
}

void loop() {
  if (digitalRead(reset)){
    analogWrite(analogOutPin,0);
  }else{
    analogWrite(analogOutPin,3);
  }
}
