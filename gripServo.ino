#include <Servo.h> 
Servo grip;
int servoPort = 3;
int angle = 0;
String cmd = "";

void setup() {
  Serial.begin(115200);
  grip.attach(servoPort);
  Serial.println("SETUP DONE");
}
void doServoAction(String cmd){
  if(cmd.compareTo("RELEASE")){
    Serial.println("RELEASING...");
    grip.write(180);
    Serial.println("DONE");
  }
  else if(cmd.compareTo("CUT")){
    Serial.println("CUTTING...")
    grip.write(0);
    Serial.println("DONE");
  }
  else{
    Serial.println("INPUT NOT RECOGNIZED: " + cmd + ". PLEASE TRY AGAIN");
  }
}
String readSerial(){
    String s = "";
    while(Serial.available()){
      s += (char)Serial.read();
    }
    return s;
}
void loop() {
  if(Serial.available()){
    cmd = readSerial();
    Serial.println("SERIAL INPUT RECIEVED: " + cmd);
    doServoaction(cmd);
  }
}

//B-W   black-gnd white-3.7V 2A
//B-W-G black-gnd white-5V arduino  green-data@servoPort
//The servo response only over/under a threshold, 0 to grip and 180 to release seems to work
