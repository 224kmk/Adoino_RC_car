#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "WiFi.h"

WiFiServer camServer(80);
  
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

  camServer.begin();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println(":80' to stream");  
}

void loop() {
  WiFiClient client = camServer.available();

  if (client) {
    Serial.println("New Client."); 
    while (client.connected()) { 
    
    }
  }
}
