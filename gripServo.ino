#include <Servo.h> 
Servo grip;
int servoPort = 3;
int angle = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  grip.attach(servoPort);
  Serial.println("Started");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    int cmd = Serial.readStringUntil('\n').toInt();
    Serial.println(int(cmd));
    grip.write(int(cmd));
  }
}

//BW black-gnd white-3.7V 2A
//BWG black-gnd white-5Varduino green-data@servoPort
