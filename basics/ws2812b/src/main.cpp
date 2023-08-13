#include <Arduino.h>
#include <NeoPixelBus.h>

#define PIN 13
#define NUMPIXEL 10
// See https://github.com/Makuna/NeoPixelBus/wiki/ESP32-NeoMethods  
// Four Channels are possible to achieve higher framerates.
#define PIXELCONFIG NeoPixelBus<NeoRgbFeature, NeoEsp32Rmt0800KbpsMethod>


PIXELCONFIG pixels(NUMPIXEL, PIN);

RgbColor black = {0,0,0};


void setup() {
  pixels.Begin();
  pixels.ClearTo(black);
  Serial.begin(115200);
}

float base = 0.0;
void loop() {
  for (int i=0; i<NUMPIXEL; i++) {
    float h = base + ((float)i)/NUMPIXEL;
    h = h - floor(h);
    pixels.SetPixelColor(i, RgbColor(HslColor(h, 1.0, 0.2)));
  }
  pixels.Show();
  base += 0.01;
  if (base>=1.0) {
    base = base-floor(base);
  }
  Serial.printf("hue = %.2f\n", base);
  delay(100);
}
