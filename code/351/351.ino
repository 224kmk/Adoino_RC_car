const int DO[] = {13,14};
uint8_t right, left;

void setup() {
  
  Serial.begin(115200);

  for(int i=0;i<sizeof(DO)/sizeof(DO[0]);i++)
    pinMode(DO[i], INPUT);
}

void loop() {
  
  right = digitalRead(DO[0]);
  left = digitalRead(DO[1]);

  Serial.print("left: ");
  Serial.print(left);
  Serial.print("  right: ");
  Serial.print(right);
  Serial.println();

  delay(100);
  
}
