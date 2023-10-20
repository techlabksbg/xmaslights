#include <NeoPixelBus.h>

#define PIN0 13
#define PIN1 12
#define PIN2 14
#define PIN3 27

class MyPixels {
    NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt0800KbpsMethod>* pixels0;
    NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt1800KbpsMethod>* pixels1;
    NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt2800KbpsMethod>* pixels2;
    NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt3800KbpsMethod>* pixels3;

    RgbColor black = {0,0,0};

    size_t bytesWritten = 0;
    uint8_t* curBuf = nullptr;
    int curStrip = 0;

    void nextBuffer() {
        curStrip+=1;
        if (curStrip==1) {
            curBuf = pixels1->Pixels();
        } else if (curStrip==2) {
            curBuf = pixels2->Pixels();
        } else if (curStrip==3) {
            curBuf = pixels3->Pixels();
        } else  {
            curStrip = 0;
            curBuf = pixels0->Pixels();
        }
        bytesWritten = 0;
    }

public:
    MyPixels() {
        pixels0 = new NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt0800KbpsMethod>(200,PIN0);
        pixels1 = new NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt1800KbpsMethod>(200,PIN1);
        pixels2 = new NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt2800KbpsMethod>(200,PIN2);
        pixels3 = new NeoPixelBus<NeoGrbFeature, NeoEsp32Rmt3800KbpsMethod>(200,PIN3);
    }

    void Begin() {
        pixels0->Begin();
        pixels1->Begin();
        pixels2->Begin();
        pixels3->Begin();
    }

    void ClearTo(RgbColor c) {
        pixels0->ClearTo(c);
        pixels1->ClearTo(c);
        pixels2->ClearTo(c);
        pixels3->ClearTo(c);
    }

    void resetBuffer() {
        bytesWritten = 0;
        curBuf = pixels0->Pixels();
        curStrip = 0;
    }

    void writeBuffer(uint8_t* source, size_t numbytes) {
        if (bytesWritten+numbytes<=600) {
            memcpy(curBuf, source, numbytes);
            curBuf+=numbytes;
            bytesWritten += numbytes;
            if (bytesWritten==600) {
                nextBuffer();
            }
        } else {
            memcpy(curBuf, source, 600-bytesWritten);
            nextBuffer();
            writeBuffer(source+600-bytesWritten, numbytes-(600-bytesWritten));
        }
        
    }

    int PixelCount() {
        return 800;
    }

    int PixelSize() {
        return 3;
    }

    void SetPixelColor(int nr, RgbColor c) {
        if (nr<200) {
            pixels0->SetPixelColor(nr % 200, c);
        } else if(nr<400) {
            pixels1->SetPixelColor(nr % 200, c);
        } else if(nr<600) {
            pixels2->SetPixelColor(nr % 200, c);
        } else if(nr<800) {
            pixels3->SetPixelColor(nr % 200, c);
        } 
    }

    void Show() {
        pixels0->Dirty();
        pixels1->Dirty();
        pixels2->Dirty();
        pixels3->Dirty();
        pixels0->Show();
        pixels1->Show();
        pixels2->Show();
        pixels3->Show();
    }
};

