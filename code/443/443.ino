#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "WiFi.h"

WiFiServer motServer(80);
  
const char* ssid = "LAPTOP-VLQHP1Q3 7270";
const char* password = "C49661=b";

const int DO[] = {13,14}; // 적외선 센서 핀을 카메라 모듈의 핀으로 연결 
uint8_t right, left, rl;

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

  Serial.begin(115200);

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

  for(int i=0;i<sizeof(DO)/sizeof(DO[0]);i++)
    pinMode(DO[i], INPUT);
}

void loop() {
  WiFiClient client = motServer.available();

  if (client) {
    Serial.println("New Client."); 
    while (client.connected()) {    
      if(client.available()) {        
        char cmd = client.read();

        if(cmd==34) {

          // capture sensor data
          right = digitalRead(DO[0]);
          left = digitalRead(DO[1]);
          // printf("%d\n", rl);

          // prepare sensor data
          rl = right<<1|left<<0;

          // send sensor data
          client.write(
            (const uint8_t *)&rl, 
            sizeof(rl));
            
        } else if(cmd==56) {
          
          char rl = client.read();
          printf("\n%d\n", rl);
          
        }
      }
    } 
  }
}
