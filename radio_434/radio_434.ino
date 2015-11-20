
#define SWITCHON  "10"
#define SWITCHOFF "01"

#define SENDER_DATA_PIN A0

// 10101     00101100  11
// preamble  payload   sync

String queue = "test";

void setup() {
  pinMode(SENDER_DATA_PIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (queue.length > 0) {
    sendCode(queue);
    queue = "";
  }
}

void serialEvent() {
  Serial.println();
}

boolean sendCode(String code){
  for(short z = 0; z<7; z++){ // repeat the code 7x
    for(short i = 0; i<12; i++){ // codelength 12 bits
      sendByte(code[i]);
    }
  sendByte('x'); // send sync code
  }
}
 
void sendByte(char i) {
  switch(i){
  case '0':{
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1); 
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(3);
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(3);
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(1);
    return;
  }
  case '1':{ 
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1);
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(3);
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1);
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(3);
    return;
  }
  case 'x':{
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1);
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(31);
  }
  }
}
 
void wait(int x) {
  delayMicroseconds(x*350); // wait x*350us
}
