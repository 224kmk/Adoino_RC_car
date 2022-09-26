#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "WiFi.h"

#define CAMERA_MODEL_M5STACK_PSRAM
#include "camera.h"

WiFiServer camServer(80);
ESP32Camera camera;
  
const char* ssid = "LAPTOP-VLQHP1Q3 7270";
const char* password = "C49661=b";

String hostname = "ESP32 Cam Server";
 
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

  camServer.begin();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println(":80' to stream");   

  camera.begin(FRAMESIZE_QQVGA, PIXFORMAT_JPEG); 
}

void loop() {
  WiFiClient client = camServer.available();

  if (client) {
    Serial.println("New Client."); 
    while (client.connected()) {      
      if(client.available()) {
        char cmd = client.read();

        if(cmd==12) {

          // capture camera data
          camera_fb_t *fb = esp_camera_fb_get(); 

          // send camera data
          client.write(
            (const uint8_t *)&fb->len, 
            sizeof(fb->len));
          client.write(
            (const uint8_t *)fb->buf, 
            fb->len);

          esp_camera_fb_return(fb);
          
        } 
      }     
    }
  }
}
