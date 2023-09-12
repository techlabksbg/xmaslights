#include <Arduino.h>
#include <WiFi.h>

// From https://randomnerdtutorials.com/get-change-esp32-esp8266-mac-address-arduino/

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.print("ESP Board MAC Address:  ");
  Serial.println(WiFi.macAddress());
}

void loop() {

}