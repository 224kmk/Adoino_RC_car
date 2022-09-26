#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

extern const int SPEED_MAX_FB;

void setup() {   
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 

  Serial.begin(115200);

  initMotor();

  // go forward speed up
  for(int spd=0;spd<SPEED_MAX_FB;spd++) {  
    turnLeft(spd);
    delay(10);
  }

  delay(1000);

  stopMotor();

  delay(1000);

  // go backward speed up
  for(int spd=0;spd<SPEED_MAX_FB;spd++) {
    turnRight(spd); 
    delay(10);
  }

  delay(1000);

  stopMotor(); 
}

void loop() { 

}
