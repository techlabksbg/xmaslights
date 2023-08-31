#include <Arduino.h>
#include <NeoPixelBus.h>

// This code is extended from https://github.com/me-no-dev/ESPAsyncWebServer/blob/master/examples/CaptivePortal/CaptivePortal.ino


#include <DNSServer.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include "ESPAsyncWebServer.h"

#include "FS.h"
#include "SPIFFS.h"

#include "secrets.h"

#define PIN 13
#define NUMPIXEL 10
// See https://github.com/Makuna/NeoPixelBus/wiki/ESP32-NeoMethods  
// Four Channels are possible to achieve higher framerates.
#define PIXELCONFIG NeoPixelBus<NeoRgbFeature, NeoEsp32Rmt0800KbpsMethod>


PIXELCONFIG pixels(NUMPIXEL, PIN);

RgbColor black = {0,0,0};

DNSServer dnsServer;
AsyncWebServer server(80);

// Globale Variablen
bool state = false;
bool newstate = state;

float pwm = 0.25;
float newpwm = pwm;

int led = 0;
int newled = led;

class CaptiveRequestHandler : public AsyncWebHandler {
public:
  CaptiveRequestHandler() {}
  virtual ~CaptiveRequestHandler() {}

  bool canHandle(AsyncWebServerRequest *request){
    //request->addInterestingHeader("ANY");
    return true;
  }

  void handleRequest(AsyncWebServerRequest *request) {
    Serial.println("CaptiveRequestHander::handleRequest");
    request->send(SPIFFS, "/index.html");
  }
};

// From https://github.com/me-no-dev/ESPAsyncWebServer/tree/master#handlers-and-how-do-they-work

// Handlers are evaluated in the order they are attached to the server.

void setupServer(){
    
  server.on("/cmd", HTTP_GET, [] (AsyncWebServerRequest *request) {
      if (request->hasParam("state")) {
        newstate = (request->getParam("state")->value() == "on");
        Serial.print("newstate ");
        Serial.println(newstate);
      }
      if (request->hasParam("pwm")) {
        newpwm = atof(request->getParam("pwm")->value().c_str());
        Serial.println(newpwm);
        if (newpwm<0.0 || newpwm>1.0) {
          newpwm = pwm;
        }
      }
      if (request->hasParam("led")) {
        newled = (request->getParam("led")->value() != "led");
        Serial.print("newled ");
        Serial.println(newled);
      request->send(200, "text/plain", "OK");
  });

  // Static files
  server.serveStatic("/index.html", SPIFFS, "/index.html");
  server.serveStatic("/led.js", SPIFFS, "/led.js");
  server.serveStatic("/led.css", SPIFFS, "/led.css");

}


// From https://techtutorialsx.com/2019/02/23/esp32-arduino-list-all-files-in-the-spiffs-file-system/
void showFiles() {
  Serial.println("Files on SPIFFS:\n");
  File root = SPIFFS.open("/");
  File file = root.openNextFile();
  while(file) {
      Serial.print("FILE: ");
      Serial.println(file.name());
      file = root.openNextFile();
  }
}

void setup(){
  //your other setup stuff...
  Serial.begin(115200);

  if(!SPIFFS.begin(true)){
    Serial.println("An Error has occurred while mounting SPIFFS");
  } else {
    Serial.println("mounted SPIFFS");
    showFiles();
  }
   

  Serial.println();
  Serial.println("Setting up AP Mode");
  WiFi.mode(WIFI_AP); 
  WiFi.softAP(MY_SSID);
  Serial.print("AP IP address: ");Serial.println(WiFi.softAPIP());
  Serial.println("Setting up Async WebServer");
  setupServer();
  Serial.println("Starting DNS Server");
  dnsServer.start(53, "*", WiFi.softAPIP());
  server.addHandler(new CaptiveRequestHandler()).setFilter(ON_AP_FILTER);//only when requested from AP
  //more handlers...
  server.begin();

  Serial.println("Setup LED");
  pixels.Begin();
  pixels.ClearTo(black);
  Serial.begin(115200);
  Serial.println("All Done!");

}

void loop(){
  dnsServer.processNextRequest();
  if (state!=newstate || newpwm != pwm || newled != led){
    state = newstate;
    pwm = newpwm;
    led = newled;
    if (!state) {
      pixels.SetPixelColor(led, RgbColor(HslColor(h, 1.0, 0.2)));
      pixels.Show();
  }
  
    } else {
      ledcWrite(0, pwm*8191);
    }  
  }



#include <Arduino.h>





//void loop() {
//  for (int i=0; i<NUMPIXEL; i++) {
//    float h = base + ((float)i)/NUMPIXEL;
//    h = h - floor(h);
//    pixels.SetPixelColor(i, RgbColor(HslColor(h, 1.0, 0.2)));
//  }
//}
