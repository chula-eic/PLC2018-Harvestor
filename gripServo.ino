#include <Servo.h> 
Servo grip;
int servoPort = 3;
int motorA = 5;
int motorB = 6;
int angle = 0;
int motorPower = 200;
String cmd = "";

void setup() {
  pinMode(motorA,OUTPUT);
  pinMode(motorB,OUTPUT);
  analogWrite(motorA,0);
  analogWrite(motorB,0);
  Serial.begin(115200);
  grip.attach(servoPort);
  Serial.println("SETUP DONE");
}
void doServoAction(String cmd){
  if(cmd == "RELEASE"){
    Serial.println("RELEASING");
    grip.write(180);
    Serial.println("DONE");
  }
  else if(cmd == "CUT"){
    Serial.println("CUTTING");
    grip.write(0);
    Serial.println("DONE");
  }
  else if (cmd == "FORWARD") {
    Serial.println("Going Forward");
    analogWrite(motorA,motorPower);
    analogWrite(motorB,0);
  }
  else if (cmd == "STOP") {
    analogWrite(motorA,0);
    analogWrite(motorB,0);
    Serial.println("Stopped");
  }
  else if (cmd == "BACKWARD") {
    Serial.println("Going Backward");
    analogWrite(motorA,0);
    analogWrite(motorB,motorPower);
  }
  else{
    Serial.println("INPUT NOT RECOGNIZED: " + cmd + ". PLEASE TRY AGAIN");
  }
}

void loop() {
  if(Serial.available()){
    cmd = Serial.readString();
    //if operated manually, use Serial.readStringUntil('\n') instead.
    Serial.println("SERIAL INPUT RECIEVED: " + cmd);
    doServoAction(cmd);
  }
}

//B-W   black-gnd white-3.7V 2A
//B-W-G black-gnd white-5V arduino  green-data@servoPort
//The servo response only over/under a threshold, 0 to grip and 180 to release seems to work
//armMotor driven as 12V DC Motor, tested with motor drive
