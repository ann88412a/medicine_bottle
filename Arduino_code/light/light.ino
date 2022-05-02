#define light_pin 5
void setup() {
  pinMode(light_pin, OUTPUT);
  Serial.begin(9600);
  Serial.println("Serial bound rate is '9600'");
  Serial.println("Please input the value of Luminous(0~255).");
}
int var_light = 10;
void loop() {
  Serial.print("Luminous value: ");
  Serial.println(var_light);
  analogWrite(light_pin, var_light);
  while(!Serial.available()){}
  String var_read = Serial.readString();
  var_light = var_read.toInt();
}
