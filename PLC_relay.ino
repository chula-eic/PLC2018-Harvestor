int r0 = 7;
int r1 = 6;
int r2 = 5;
int r3 = 4;


char cmd = '0';

void setup() {
  pinMode(r0,OUTPUT);
  pinMode(r1,OUTPUT);
  pinMode(r2,OUTPUT);
  pinMode(r3,OUTPUT);
  digitalWrite(r0, HIGH);
  digitalWrite(r1, HIGH);
  digitalWrite(r2, HIGH);
  digitalWrite(r3, HIGH);
  Serial.begin(9600);
  Serial.println("SETUP DONE");
}

void loop() {
  if(Serial.available()){
    cmd = Serial.read();
    //if operated manually, use Serial.readStringUntil('\n') instead.
    Serial.println("SERIAL INPUT RECIEVED: " + cmd);
    if(cmd == '0'){
      digitalWrite(r0, HIGH);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, HIGH);
    }
    else if(cmd == '1'){
      digitalWrite(r0, LOW);
      digitalWrite(r1, LOW);
      digitalWrite(r2, LOW);
      digitalWrite(r3, LOW);
    }
    else if(cmd == '2'){
      digitalWrite(r0, HIGH);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, LOW);
      digitalWrite(r3, HIGH);
    }
    else if(cmd == '3'){
      digitalWrite(r0, HIGH);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, LOW);
      digitalWrite(r3, LOW);
    }
    else if(cmd == '4'){
      digitalWrite(r0, HIGH);
      digitalWrite(r1, LOW);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, HIGH);
    }
    else if(cmd == '5'){
      digitalWrite(r0, HIGH);
      digitalWrite(r1, LOW);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, LOW);
    }
    else if(cmd == '6'){
      digitalWrite(r0, HIGH);
      digitalWrite(r1, LOW);
      digitalWrite(r2, LOW);
      digitalWrite(r3, HIGH);
    }
    else if(cmd == '7'){
      digitalWrite(r0, HIGH);
      digitalWrite(r1, LOW);
      digitalWrite(r2, LOW);
      digitalWrite(r3, LOW);
    }
    else if(cmd == '8'){
      digitalWrite(r0, LOW);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, HIGH);
    }
    else if(cmd == '9'){
      digitalWrite(r0, LOW);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, LOW);
    }
    else{
      digitalWrite(r0, HIGH);
      digitalWrite(r1, HIGH);
      digitalWrite(r2, HIGH);
      digitalWrite(r3, HIGH);
    }
    delay(2500);
  }
  delay(100);
  digitalWrite(r0, HIGH);
  digitalWrite(r1, HIGH);
  digitalWrite(r2, HIGH);
  digitalWrite(r3, HIGH);
}
