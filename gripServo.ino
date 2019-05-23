#include <Servo.h> 
Servo grip;
int servoPort = 3;
int angle = 0;

void setup() {
  Serial.begin(115200);
  grip.attach(servoPort);
  Serial.println("Started");
}

void loop() {
  if(Serial.available() > 0){
    int cmd = Serial.readStringUntil('\n').toInt();
    Serial.println(int(cmd));
    grip.write(int(cmd));
  }
}

//B-W   black-gnd white-3.7V 2A
//B-W-G black-gnd white-5V arduino  green-data@servoPort
//The servo response only over/under a threshold, 0 to grip and 180 to release seems to work
