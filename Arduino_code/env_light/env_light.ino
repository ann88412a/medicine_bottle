#define light_pin 5 //define the light hardware pin is D5(PWM)
#define serial_bound_rate 115200 //defint the bound rate is 115200
uint8_t var_light = 10; //init val is 10
String serial_read = ""; //init
bool DEBUG_MODE = false; //serial print info (if true)

void setup() {
  pinMode(light_pin, OUTPUT); //set light pin is output
  Serial.begin(serial_bound_rate); //set bound rate
  Serial.setTimeout(10); //set serial timeout (readString wait time)
  analogWrite(light_pin, var_light); //init the light
  if (DEBUG_MODE) {
    Serial.println("Serial bound rate is '" + String(serial_bound_rate) + "'");
    Serial.println("Please input the value of Luminous(0~255).");
  }
}

void loop() {
  if (serial_read.length() > 2) {
    var_light = serial_read.toInt(); //str => int
    analogWrite(light_pin, var_light); //set light val

    if (DEBUG_MODE) {
      Serial.println("Luminous value: " + String(var_light)); // print the light val
    }
  }

  while (!Serial.available()) {} //wait for input
  serial_read = Serial.readString(); //read input

}
