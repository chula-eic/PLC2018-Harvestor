#include <Servo.h> 
Servo grip, catcher1,catcher2;
int servoGripPort = 3;
int servoCatcher1 = 9;
int servoCatcher2 = 10;
int motorA = 5;
int motorB = 6;
int V5 = 8; //5v replacement
int frntLimPin = 12;
int backLimPin = 13;
int angle = 0;
int motorPower = 200;
bool FW = false;
bool BW = false;

String cmd = "";

void setup() {
  pinMode(motorA,OUTPUT);
  pinMode(motorB,OUTPUT);
  pinMode(frntLimPin,INPUT);
  pinMode(backLimPin,INPUT);
  pinMode(V5,OUTPUT);
  digitalWrite(V5,HIGH);
  analogWrite(motorA,0);
  analogWrite(motorB,0);
  Serial.begin(115200);
  grip.attach(servoGripPort);
  catcher1.attach(servoCatcher1);
  catcher2.attach(servoCatcher2);
  Serial.print("SETUP DONE");
}
void doServoAction(String cmd){
  if(cmd == "RELEASE"){
    Serial.print("RELEASING");
    grip.write(180);
    Serial.print("DONE");
  }
  else if(cmd == "CUT"){
    Serial.print("CUTTING");
    grip.write(0);
    Serial.print("DONE");
  }
  else if (cmd == "FORWARD") {
    Serial.print("Going Forward");
    analogWrite(motorA,motorPower);
    analogWrite(motorB,0);
    FW = true;
    BW = false;
  }
  else if (cmd == "STOP") {
    analogWrite(motorA,0);
    analogWrite(motorB,0);
    Serial.print("Stopped");
    FW = false;
    BW = false;
  }
  else if (cmd == "BACKWARD") {
    Serial.print("Going Backward");
    analogWrite(motorA,0);
    analogWrite(motorB,motorPower);
    FW = false;
    BW = true;
  }
  else if(cmd == "CLOSE"){
    Serial.print("Closing the catcher");
    catcher1.write(90);
    catcher2.write(90);
    Serial.print("DONE");
  }
  else if(cmd == "OPEN"){
    Serial.print("Opening the catcher");
    catcher1.write(180);
    catcher2.write(0);
    Serial.print("DONE");
  }
  else{
    Serial.print("INPUT NOT RECOGNIZED: " + cmd + ". PLEASE TRY AGAIN");
  }
}

void loop() {
  if(Serial.available()){
    cmd = Serial.readString();
    //if operated manually, use Serial.readStringUntil('\n') instead.
    Serial.print("SERIAL INPUT RECIEVED: " + cmd);
    doServoAction(cmd);
  }
  //Serial.print(String(digitalRead(frntLimPin))+" "+String(digitalRead(backLimPin)));
  if ((FW && digitalRead(frntLimPin)==1)||(BW && digitalRead(backLimPin)==1)) {Serial.print("Limit Reached. Forcing STOP Command");doServoAction("STOP");}
}

//B-W   black-gnd white-3.7V 2A
//B-W-G black-gnd white-5V arduino  green-data@servoGripPort
//The servo response only over/under a threshold, 0 to grip and 180 to release seems to work
//armMotor driven as 12V DC Motor, tested with motor drive
//Limit Switch Board sequence +FB- hole on the right, top view

//Catcher have not tested together yet, but one of them works for sure.