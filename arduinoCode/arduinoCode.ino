#include <Servo.h>

Servo motor1;
Servo motor2;
Servo motor3;
#define motorPin1 9
#define motorPin2 10
#define motorPin3 11

void setup() {
  // put your setup code here, to run once:
  motor1.attach(motorPin1);
  motor1.writeMicroseconds(1500);
  
  motor2.attach(motorPin2);
  motor2.writeMicroseconds(1500);
  
  motor3.attach(motorPin3);
  motor3.writeMicroseconds(1500);

  Serial.begin(9600);
  delay(5000);
}

void loop() {
  // m~xxxx
  // ~ is motor number
  // xxxx is motor control 1000-1500-2000

  if (Serial.available() >= 6) {  
    char command[7];  
    Serial.readBytesUntil('\n', command, 6);
    command[6] = '\0';

    if (command[0] == 'm') {
      int motor = command[1] - '0';
      int speed = atoi(command + 2);
      
      Serial.println(motor);
      Serial.println(speed);

      if (motor == 1) {
        motor1.writeMicroseconds(speed);
      }

      if (motor == 2) {
        motor2.writeMicroseconds(speed);
      }

      if (motor == 3) {
        motor3.writeMicroseconds(speed);
      }
      
    }
  }                      
}
