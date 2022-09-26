const int dcMotors[] = {16,17,22,21,12,27,25,26};
const int mot_channels[] = {0,1,2,3};
const int mot_freq = 10000;
const int mot_res = 10;

const int SPEED_MIN = 256;
const int SPEED_MAX = 1024;

const int forward[] = {HIGH,LOW};
const int backward[] = {LOW,HIGH};
const int stop[] = {LOW,LOW};

const int SPEED_MAX_FB = SPEED_MAX - SPEED_MIN;

void initMotor() {  
  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {
    pinMode(dcMotors[i], OUTPUT);
    ledcAttachPin(dcMotors[i+1], mot_channels[i/2]);
    ledcSetup(mot_channels[i/2], mot_freq, mot_res);
  }
}

void goForward(long spd) {
    
  if(spd<0) spd=0;
  spd += SPEED_MIN;
  if(spd>SPEED_MAX) spd = SPEED_MAX;

  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {  
    digitalWrite(dcMotors[i], forward[i%2]);
    ledcWrite(mot_channels[i/2], SPEED_MAX-spd);
  }

}

void stopMotor() { 
  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {
    digitalWrite(dcMotors[i], stop[i%2]);
    ledcWrite(mot_channels[i/2], 0);
  }
}

void goBackward(long spd) {

  if(spd<0) spd=0;
  spd += SPEED_MIN;
  if(spd>SPEED_MAX) spd = SPEED_MAX;

  for(int i=0;i<sizeof(dcMotors)/sizeof(dcMotors[0]);i+=2) {
    digitalWrite(dcMotors[i], backward[i%2]);
    ledcWrite(mot_channels[i/2], spd);
  }
  
}

void turnLeft(long spd) {

  if(spd<0) spd=0;
  spd += SPEED_MIN;
  if(spd>SPEED_MAX) spd = SPEED_MAX; 

  for(int i=0;i<4;i+=2) {
    digitalWrite(dcMotors[i], forward[i%2]);
    ledcWrite(mot_channels[i/2], SPEED_MAX - spd);
  }

  for(int i=4;i<8;i+=2) { 
    digitalWrite(dcMotors[i], backward[i%2]); 
    ledcWrite(mot_channels[i/2], spd);
  }
  
}

void turnRight(long spd) {

  if(spd<0) spd=0;
  spd += SPEED_MIN;
  if(spd>SPEED_MAX) spd = SPEED_MAX; 

  for(int i=0;i<4;i+=2) {
    digitalWrite(dcMotors[i], backward[i%2]); 
    ledcWrite(mot_channels[i/2], spd);
  }
   
  for(int i=4;i<8;i+=2) {
    digitalWrite(dcMotors[i], forward[i%2]);
    ledcWrite(mot_channels[i/2], SPEED_MAX - spd);
  }
  
}
