const int led_pin = 2;
const int led_channel = 1;
const int led_freq = 100;
const int led_resolution = 10;

void setup() {
  ledcAttachPin(led_pin, led_channel);
  ledcSetup(led_channel, led_freq, led_resolution);

  ledcWrite(led_channel, 0);
}

void loop() {

  for(int t_high=0;t_high<=1024;t_high++) {   
    ledcWrite(led_channel, t_high);
    delay(1);   
  }

}
