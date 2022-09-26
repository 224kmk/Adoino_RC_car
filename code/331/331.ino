const int led_pin = 2;
const int led_channel = 1;
const int led_freq = 1;
const int led_resolution = 10;

void setup() {
  ledcAttachPin(led_pin, led_channel);
  ledcSetup(led_channel, led_freq, led_resolution);

  ledcWrite(led_channel, 100);
}

void loop() {

}
