#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "WiFi.h"

WiFiServer motServer(80);
  
const char* ssid = "LAPTOP-VLQHP1Q3 7270";
const char* password = "C49661=b";

String hostname = "ESP32 Mot Server";
 
void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 

  Serial.begin(115200);

  WiFi.config(INADDR_NONE, INADDR_NONE, 
    INADDR_NONE, INADDR_NONE);
  WiFi.setHostname(hostname.c_str()); //define hostname

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  motServer.begin();

  Serial.print("Motor Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println(":80' to drive");

  initMotor();
}

long speedFwd = 128; // speed for 0~768
long speedCurve = 128; // speed for 0~768

void loop() {
  WiFiClient client = motServer.available();

  if (client) {
    Serial.println("New Client."); 
    while (client.connected()) {    
      if(client.available()) {
                  
        char rl = client.read();

        int right = (rl&2)>>1;
        int left = (rl&1)>>0;

        if (right==0 && left==0) {
          goForward(speedFwd);
        } else if (right==0&& left==1 ) {
          turnRight(speedCurve);
        } else if (right==1 && left==0) {
          turnLeft(speedCurve);
        } else if (right==1 && left==1) {
          stopMotor();
        }          
              
      }   
    } 
    
    stopMotor();
    
  }
}
