//lighbar sketch for the HackIAA2017
//github.com/RBEGamer

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
#define PIN            4
#define NUMPIXELS      8


Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);



void setup() {
  Serial.begin(115200);
  pixels.begin(); // This initializes the NeoPixel library.
}


String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {
    0, -1  };
  int maxIndex = data.length()-1;
  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
      found++;
      strIndex[0] = strIndex[1]+1;
      strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

String str = "";
int v1 = 0;
int v2 = 0;
void loop() {

  
if(Serial.available() > 0)
    {
        str = Serial.readStringUntil('\n');

        v1 = getValue(str,'_',0).toInt();
        v2 = getValue(str,'_',1).toInt();
    }

    if(v1 == 0){
  for(int i=0;i<4;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(0,0,30)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
    }

        if(v1 == 1){
  for(int i=0;i<4;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(128,70,0)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
    }

            if(v1 == 2){
  for(int i=0;i<4;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(255,50,0)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
    }

                if(v1 == 3){
  for(int i=0;i<4;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(255,0,0)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
    }



        if(v2 == 0){
  for(int i=4;i<8;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(0,0,30)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
    }

        if(v2 == 1){
  for(int i=4;i<8;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(128,70,0)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
    }

            if(v2 == 2){
  for(int i=4;i<8;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(255,50,0)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
    }

                if(v2 == 3){
  for(int i=4;i<8;i++){
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(255,0,0)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
  }
    }
   delay(100); // Delay for a period of time (in milliseconds).
}
