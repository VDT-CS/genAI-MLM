void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.print("A0: ");
  Serial.print(analogRead(A0));
  Serial.print(" A1: ");
  Serial.print(analogRead(A1));
  Serial.print(" A2: ");
  Serial.print(analogRead(A2));
  Serial.print(" A3: ");
  Serial.println(analogRead(A3));
  delay(1000); // Update every second
}