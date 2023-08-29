#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  ledcSetup(0, 500, 13);  // Kanal 0, 500 Hz, 13 Bits Auflösung (maximale Bittiefe hängt von der Frequenz ab)
  ledcAttachPin(BUILTIN_LED, 0); // PWM Generator für Pin 2 mit Kanal 0
}

void loop() {
  unsigned int t = millis()%2000;
  if (t>1000) {
    t = 2000-t;
  }
  float v = 0.001*t;
  if (digitalRead(0)) { // Wenn der Button "boot" HIGH liefert (d.h. nicht gedrückt ist), inverse Logik
    v = pow(v, 2.5);  // Gamma Faktor
  }
  t = 8191*v;
  // Serial.println(t);
  ledcWrite(0, t); // Kanal 0
  delay(1);
}
