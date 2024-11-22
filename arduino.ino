#define BUZZER_PIN 3
#define LIGHTS_PIN 4
#define MOTOR_PIN 5

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LIGHTS_PIN, OUTPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command == "ALERT") {
      digitalWrite(BUZZER_PIN, HIGH); // Turn on buzzer
      digitalWrite(LIGHTS_PIN, HIGH); // Turn on emergency lights
      analogWrite(MOTOR_PIN, 128);    // Reduce motor speed (simulate slowing)
    } else if (command == "RESET") {
      digitalWrite(BUZZER_PIN, LOW);  // Turn off buzzer
      digitalWrite(LIGHTS_PIN, LOW); // Turn off emergency lights
      analogWrite(MOTOR_PIN, 255);   // Full motor speed (normal state)
    }
  }
}
