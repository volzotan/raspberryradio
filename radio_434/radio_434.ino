
#define SENDER_DATA_PIN A0

#define DEBUG

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

void convert(char binaryrep[], char payload) {
  #ifdef DEBUG
    Serial.println(payload, BIN);
  #endif
  
  int paritybit = 0;
  
  for (int j=0; j<8; j++) { 
    if (payload & (1 << j)) {
      binaryrep[j] = '1';
      paritybit++;
    } else {
      binaryrep[j] = '0';
    }
  }
  
  binaryrep[8] = (paritybit % 2) + 48; // 1 -> '1'
}

void sendMessage(char payload) {
  char binaryrep[9] = {0};
  convert(binaryrep, payload);

  sendBit('p'); // preamble
  
  for (int i=0; i<sizeof(binaryrep); i++) {
    sendBit(binaryrep[i]);
  }
   
  sendBit('x'); // sync
}
 
void sendBit(char i) {
  #ifdef DEBUG
    Serial.println(i);
  #endif
  
  switch(i){
    case '0':{
      digitalWrite(SENDER_DATA_PIN,HIGH);
      wait(2); 
      digitalWrite(SENDER_DATA_PIN,LOW);
      wait(3);
      return;
    }
    case '1':{ 
      digitalWrite(SENDER_DATA_PIN,HIGH);
      wait(4); 
      digitalWrite(SENDER_DATA_PIN,LOW);
      wait(1);
      return;
    }
    case 'p':{
      digitalWrite(SENDER_DATA_PIN,HIGH);
      wait(1);
      digitalWrite(SENDER_DATA_PIN,LOW);
      wait(1);
      digitalWrite(SENDER_DATA_PIN,HIGH);
      wait(3);
      digitalWrite(SENDER_DATA_PIN,LOW);
      wait(1);
      digitalWrite(SENDER_DATA_PIN,HIGH);
      wait(1);
      digitalWrite(SENDER_DATA_PIN,LOW);
      wait(1);
      return;
    }
    case 'x':{
      digitalWrite(SENDER_DATA_PIN,HIGH);
      wait(1);
      digitalWrite(SENDER_DATA_PIN,LOW);
      wait(1);
      digitalWrite(SENDER_DATA_PIN,HIGH);
      wait(1);
      digitalWrite(SENDER_DATA_PIN,LOW);
      wait(1);
      return;
    }
  }
}
 
void wait(int x) {
  delayMicroseconds(x*350); // wait x*350us
}
