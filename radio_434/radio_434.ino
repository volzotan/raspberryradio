
#define SENDER_DATA_PIN A0

// 10101     00101100  11
// preamble  payload   sync

String queue = "test";

void setup() {
  pinMode(SENDER_DATA_PIN, OUTPUT);
  queue.reserve(500);
  Serial.begin(9600);
  
  while (!Serial) {
    ; 
  }
}

void loop() {
  serialEvent();
  if (queue.length() > 0) {
    for (int i=0; i<queue.length(); i++) {
      sendMessage(queue[i]);
    }
    queue = "";
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char) Serial.read();
    queue += inChar;
  }
}

void sendMessage(char payload) {
  sendBit('p'); // preamble
  sendPayload(payload);
  sendBit('x'); // sync
}

void sendPayload(char payload) {
  Serial.println(payload, BIN);
  for (int j=0; j<8; j++) { 
    if (payload & (1 << j)) {
      sendBit('1');
    } else {
      sendBit('0');
    }
  }
}
 
void sendBit(char i) {
  Serial.println(i);
  return;
  
  switch(i){
  case '0':{
    digitalWrite(SENDER_DATA_PIN,HIGH);
    wait(1); 
    digitalWrite(SENDER_DATA_PIN,LOW);
    wait(1);
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
