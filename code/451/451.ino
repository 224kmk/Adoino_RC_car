#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "WiFi.h"

WiFiServer motServer(80);
  
const char* ssid = "LAPTOP-VLQHP1Q3 7270";
const char* password = "C49661=b";

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
}

void loop() {
  WiFiClient client = motServer.available();

  if (client) {
    Serial.println("New Client."); 
    while (client.connected()) {    
      if(client.available()) {        
        char cmd = client.read();
        printf("\n%d\n", cmd); 
      }  
    } 
  }
}
