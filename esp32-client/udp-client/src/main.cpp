#include <Arduino.h>
#include <WiFi.h>
#include "AsyncUDP.h"
#include <NeoPixelBus.h>

#define PIN 13
#define NUMPIXEL 30 
// See https://github.com/Makuna/NeoPixelBus/wiki/ESP32-NeoMethods  
// Four Channels are possible to achieve higher framerates.
//#define PIXELCONFIG NeoPixelBus<NeoRgbFeature, NeoEsp32Rmt0800KbpsMethod>
#define PIXELCONFIG NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt0800KbpsMethod>


PIXELCONFIG pixels(NUMPIXEL, PIN);

RgbColor black = {0,0,0};




#include "secrets.h"
#define PORT 15878
#define SERVER IPAddress(192,168,178,22)

AsyncUDP udp;


// From https://randomnerdtutorials.com/esp32-useful-wi-fi-functions-arduino/#3
void initWiFi() {
  WiFi.disconnect();
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWD);
  Serial.print("Connecting to WiFi ..");
  int max = 0;
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
    pixels.SetPixelColor(max, RgbColor(20,0,0));
    max++;
    if (max>30) { 
      Serial.println("No wifi, rebooting!");
      delay(1000);
      ESP.restart();
    }
  }
  for (int i=0; i<max; i++) {
    pixels.SetPixelColor(i, RgbColor(0,20,0));
  }
  Serial.println(WiFi.localIP());
}

// From https://randomnerdtutorials.com/esp32-http-get-post-arduino/#http-get-1

// From https://randomnerdtutorials.com/get-change-esp32-esp8266-mac-address-arduino/
void showMac() {
  Serial.print("ESP Board MAC Address:  ");
  Serial.println(WiFi.macAddress());
}

unsigned long lastPing = 0;
unsigned long lastData = 0;
unsigned long start = 0;
unsigned int frames = 0;
unsigned long nextFPS = 0;

int nextPacket = 0;
size_t bytesWritten = 0;
uint8_t* bufferStart = nullptr;

void init_UDP() {
  if(udp.connect(SERVER, PORT)) {
    Serial.println("UDP connected");
    // from https://github.com/espressif/arduino-esp32/blob/master/libraries/AsyncUDP/examples/AsyncUDPClient/AsyncUDPClient.ino
    udp.onPacket([](AsyncUDPPacket packet) {
            /*Serial.print("UDP Packet Type: ");
            Serial.print(packet.isBroadcast()?"Broadcast":packet.isMulticast()?"Multicast":"Unicast"); 
            Serial.print(", From: ");
            Serial.print(packet.remoteIP());
            Serial.print(":");
            Serial.print(packet.remotePort());
            Serial.print(", To: ");
            Serial.print(packet.localIP());
            Serial.print(":");
            Serial.print(packet.localPort()); 
            Serial.print("L ");
            Serial.print(packet.length());
            Serial.print(" B0 ");
            Serial.print(packet.data()[0]); */
            uint8_t* data = packet.data();
            size_t l = packet.length();

            if (l==5 && data[0]==254) {              
              if (data[1]=='p' && data[2]=='o' && data[3]=='n' && data[4]=='g') {
                //Serial.println("pong");
              }
              return;
            }
            if (data[0]==nextPacket || data[0]==255) {
              if (nextPacket==0) {              
                bufferStart = pixels.Pixels();
              }
              memcpy(bufferStart, data+1, l-1);
              bufferStart+=l-1;
              nextPacket++;
            } else {
              //Serial.printf("expected packet %d, got %d instead\n", nextPacket, data[0]);
              nextPacket = 0;
              bufferStart = nullptr;
            }
            if (data[0]==255 && bufferStart!=nullptr) {
              pixels.Dirty();
              pixels.Show();
              bufferStart = nullptr;
              nextPacket = 0;
              if (start==0) {
                start = millis();
              }
              frames++;
            }
            lastData = millis();
        });
  }
}

void clearPixels() {
  pixels.ClearTo(black);
  pixels.Show();
}

void initPixels() {
  pixels.Begin();
  clearPixels();
}

void setup() {
  initPixels();
  Serial.begin(115200);
  delay(10);
  Serial.printf("Pixelconfig: %d pixels total, %d bytes/pixel\n", pixels.PixelCount(), pixels.PixelSize());
  showMac();
  initWiFi();
  init_UDP();
}

int noResponseCounter = 30;

void loop() {
  if (millis()-lastPing>1000) {
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("No more WiFi, rebooting...");
      delay(1000);
      ESP.restart();
    }
    if (lastData==0 || (lastData>0 && millis()-lastData>5000)) {
      Serial.println("sending start");
      lastPing=millis();
      udp.print("start");
      noResponseCounter--;
      if (noResponseCounter==0) {
        Serial.println("no response, rebooting");
        delay(1000);
        ESP.restart();
      }
    } else {
      //Serial.println("sending ping");
      lastPing=millis();
      udp.print("ping");
    }
    if (start>0 && start<millis()+1000) {
      Serial.printf("%d frames at %.1f fps\n", frames, 1000.0*frames/(millis()-start));
    }
  }
}