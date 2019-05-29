#include <Servo.h> 
Servo grip;
int servoPort = 3;
int motorA = 5;
int motorB = 6;
int V5 = 8; //5v replacement
int frntLimPin = 12;
int backLimPin = 13;
int angle = 0;
int motorPower = 200;
bool FW = false;
bool BW = false;

char cmd = 'a';


void releasu(){
    Serial.println("RELEASING");
    grip.write(180);
    Serial.println("DONE");
}
void cut(){
    Serial.println("CUTTING");
    grip.write(0);
    Serial.println("DONE");
}
void forward(){
    Serial.println("Going Forward");
    analogWrite(motorA,motorPower);
    digitalWrite(motorB,0);
    FW = true;
    BW = false;
}
void stoppu(){
    digitalWrite(motorA,0);
    digitalWrite(motorB,0);
    Serial.println("Stopped");
    FW = false;
    BW = false;
}
void backward(){
    Serial.println("Going Backward");
    digitalWrite(motorA,0);
    analogWrite(motorB,motorPower);
    FW = false;
    BW = true;
}


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
  grip.attach(servoPort);
  Serial.println("SETUP DONE");
}



void loop() {
  if(Serial.available()){
    cmd = Serial.read();
    //if operated manually, use Serial.readStringUntil('\n') instead.
    Serial.println("SERIAL INPUT RECIEVED: " + cmd);
    switch(cmd){
      case 'F':
        forward();
        break;
      case 'B': 
        backward();
        break;
      case 'S': 
        stoppu();
        break;
      case 'C': 
        cut();
        break;
      case 'R': 
        releasu();
        break;
      default:
        Serial.println("ÏNPUT NOT RECOGNIZED, PLEASE TRY AGAIN!");
        break;
    }
  }
  //Serial.println(String(digitalRead(frntLimPin))+" "+String(digitalRead(backLimPin)));
  if ((FW && digitalRead(frntLimPin)==1)||(BW && digitalRead(backLimPin)==1)) {Serial.println("Limit Reached. Forcing STOP Command");stoppu();}
  delay(50);
}

//B-W   black-gnd white-3.7V 2A
//B-W-G black-gnd white-5V arduino  green-data@servoPort
//The servo response only over/under a threshold, 0 to grip and 180 to release seems to work
//armMotor driven as 12V DC Motor, tested with motor drive
//Limit Switch Board sequence +FB- hole on the right, top view
