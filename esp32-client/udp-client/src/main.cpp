#include <Arduino.h>
#include <WiFi.h>
#include "AsyncUDP.h"
#include <NeoPixelBus.h>
#include "myPixels.h"

RgbColor black = {0,0,0};

MyPixels pixels;

#include "secrets.h"
#define PORT 15878
#define SERVER IPAddress(81,62,232,82)


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
    pixels.SetPixelColor(max, RgbColor(5,0,0));
    pixels.Show();
    delay(1000);
    
    max++;
    if (max>30) { 
      Serial.println("No wifi, rebooting!");
      delay(1000);
      ESP.restart();
    }
  }
  pixels.ClearTo(black);
  pixels.SetPixelColor(0, RgbColor(0,5,0));
  pixels.Show();
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
bool writing = false;


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
            lastData = millis();

            if (l==5 && data[0]==254) {            
              if (data[1]=='p' && data[2]=='o' && data[3]=='n' && data[4]=='g') {
                //Serial.println("pong");
              }
              return;
            }
            if (l>1 && (data[0]==nextPacket || data[0]==255)) {
              //Serial.printf("[%d], len=%d\n", nextPacket, l);
              if (nextPacket==0) {
                pixels.resetBuffer();
                writing = true;
              }
              bool full = pixels.writeBuffer(data+1, l-1);
              if (data[0]==255) {
                pixels.Show();
                writing = false;
                nextPacket = 0;
                if (start==0) {
                  start = millis();
                }
                if (full) {
                  frames++;
                } else {
                  Serial.println("  strips not full, displaying anyway??");
                }
              } else {
                nextPacket++;
              }
              return;
            } 
            Serial.printf("expected packet %d, got %d instead\n", nextPacket, data[0]);
            nextPacket = 0;
            writing = false;
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