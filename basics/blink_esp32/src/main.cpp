#include <Arduino.h>


void setup() {
  // Pin auf Output schalten
  pinMode(BUILTIN_LED, OUTPUT);
}

void loop() {
  // 3.3V auf pin 2 anlegen:
  digitalWrite(BUILTIN_LED, HIGH);
  delay(500); // halbe Sekunde warten
  digitalWrite(BUILTIN_LED, LOW);
  delay(500);
}