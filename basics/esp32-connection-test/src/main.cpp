#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

// From https://randomnerdtutorials.com/esp32-useful-wi-fi-functions-arduino/#3
void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin("KSBG-PSK", nullptr);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

// From https://randomnerdtutorials.com/esp32-http-get-post-arduino/#http-get-1

void testConnection() {
  HTTPClient http;

    String serverPath = "http://tech-lab.ch/";
    
    // Your Domain name with URL path or IP address with path
    http.begin(serverPath.c_str());
    
    // If you need Node-RED/server authentication, insert user and password below
    //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
    
    // Send HTTP GET request
    int httpResponseCode = http.GET();
    
    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
}

// From https://randomnerdtutorials.com/get-change-esp32-esp8266-mac-address-arduino/
void showMac() {
  Serial.print("ESP Board MAC Address:  ");
  Serial.println(WiFi.macAddress());
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  showMac();
  initWiFi();
  testConnection();
}


void loop() {

}