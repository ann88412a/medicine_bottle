/**

   HX711 library for Arduino - example file
   https://github.com/bogde/HX711

   MIT License
   (c) 2018 Bogdan Necula

**/
#include "HX711.h"
// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;
HX711 scale;

int sort_desc(const void *cmp1, const void *cmp2)
{
  // Need to cast the void * to int *
  int a = *((int *)cmp1);
  int b = *((int *)cmp2);
  // The comparison
  return a > b ? -1 : (a < b ? 1 : 0);
}

double get_weight(int n = 50, float err = 0.001) {
  double hist[n];
  double val, val_sum = 0;

  for (int i = 0; i < n; i++) {
    val = scale.get_units();
    hist[i] = val;
  }

  int hist_length = sizeof(hist) / sizeof(hist[0]);
  qsort(hist, hist_length, sizeof(hist[0]), sort_desc);


  double val_mid = hist[hist_length/2];
  double out_sum = 0;
  int cnt = 0;
  for (int i = 0; i < n; i++) {
    if (abs(hist[i] - val_mid) < err) {
      out_sum += hist[i];
      cnt++;
    }
  }
  double out = out_sum / cnt;
  return out;
}

double get_val, max_val = 0;
double min_val = 10000;
void setup() {
  Serial.begin(38400);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(1142.f);                      // this value is obtained by calibrating the scale with known weights; see the README for details
  scale.tare();               // reset the scale to 0
  Serial.println("put on");
  delay(3000);
  scale.get_units();
}

void loop() {
  //  Serial.println(get_weight(),4);
  //  Serial.print("one reading:\t");
  //  Serial.print(scale.get_units(), 3);
  //  Serial.print("\t| average:\t");

  get_val = get_weight();
  if (get_val > max_val) {
    max_val = get_val;
  }
  if (get_val < min_val) {
    min_val = get_val;
  }
  Serial.print("val: ");
  Serial.print(get_val, 4);
  Serial.print("\t max: ");
  Serial.print(max_val, 4);
  Serial.print("\t min: ");
  Serial.print(min_val, 4);
  Serial.print("\t err: ");
  Serial.println(max_val - min_val, 4);

  scale.power_down();             // put the ADC in sleep mode
  delay(300);
  scale.power_up();
}
