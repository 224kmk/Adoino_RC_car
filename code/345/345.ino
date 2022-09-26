#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

const int dcMotors[] = {16,17};
const int mot_channels[] = {0};
const int mot_freq = 10000;
const int mot_res = 10;

const int SPEED_MIN = 256;
const int SPEED_MAX = 1023;

const int forward[] = {HIGH,LOW};
const int backward[] = {LOW,HIGH};
const int stop[] = {LOW,LOW};

void setup() {  
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 

  Serial.begin(115200);

  // init motor
  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {
    pinMode(dcMotors[i], OUTPUT);//
    ledcAttachPin(dcMotors[i+1], mot_channels[i/2]);
    ledcSetup(mot_channels[i/2], mot_freq, mot_res);
  }
  
  // go forward
  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {  
    digitalWrite(dcMotors[i], forward[i%2]);
  }

  // speed up
  for(int spd=SPEED_MIN;spd<=SPEED_MAX;spd++) {
    for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {  
      ledcWrite(mot_channels[i/2], SPEED_MAX-spd); 
    } 
    delay(10);
  }

  delay(1000);

  // stop motor
  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {
    digitalWrite(dcMotors[i], stop[i%2]);
    ledcWrite(mot_channels[i/2], 0);
  }

  delay(1000);

  // go backward
  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {
    digitalWrite(dcMotors[i], backward[i%2]);
  }

  // speed up
  for(int spd=SPEED_MIN;spd<=SPEED_MAX;spd++) {
    for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {
      ledcWrite(mot_channels[i/2], spd); 
    }
    delay(10);
  }

  delay(1000);

  // stop motor
  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {
    digitalWrite(dcMotors[i], stop[i%2]);
    ledcWrite(mot_channels[i/2], 0);
  }   
}

void loop() {
  
}
