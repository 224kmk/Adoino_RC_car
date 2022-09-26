#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

extern const int SPEED_MAX_FB;

const int DO[] = {13,14};

void setup() {   
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 

  Serial.begin(115200);

  initMotor();

  for(int i=0;i<sizeof(DO)/sizeof(DO[0]);i++)
    pinMode(DO[i], INPUT);
}

long speedFwd = 128;
long speedCurve = 256+128;

void loop() { 
  
  uint8_t right = digitalRead(DO[0]);
  uint8_t left = digitalRead(DO[1]);

  if (left==0 && right==0) {
    goForward(speedFwd);
  } else if (left==1 && right==1) {
    stopMotor(); 
  } else if (left==0 && right==1) {
    turnLeft(speedCurve);
  } else if (left==1 && right==0) {
    turnRight(speedCurve);
  }

}
