#include <stdint.h>

const uint8_t pins[8] = {
  11, 12, 13, 14, 15, 16, 17, 18,
};

const uint8_t CS = 1;
const uint8_t SK = 2;
const uint8_t DI = 3;
const uint8_t DO = 4;
const uint8_t GND = 5;
const uint8_t TEST = 6;
const uint8_t NC = 7;
const uint8_t VCC = 8;

void setPin(uint8_t pin, uint8_t value) {
  digitalWrite(pins[pin-1],value);
}

uint8_t getPin(uint8_t pin) {
  return digitalRead(pins[pin-1]);
}

void initPin(uint8_t pin, uint8_t value, uint8_t dir) {
  pinMode(pins[pin-1],dir);
  setPin(pin,value);
}

// When you're all wired up, hit the reset button
// to start dumping the hex codes.

void setup() {
  initPin(CS,LOW,OUTPUT);
  initPin(GND,LOW,OUTPUT);
  initPin(VCC,HIGH,OUTPUT);
  initPin(DO,HIGH,INPUT);
  initPin(DI,LOW,OUTPUT);
  initPin(TEST,LOW,OUTPUT);
  initPin(SK,LOW,OUTPUT);

  Serial.begin(115200);
}

uint8_t doBit(uint8_t out) {
  setPin(DI,out);
  setPin(SK,HIGH);
  setPin(SK,LOW);
  return getPin(DO);
}

const int ADDR_BITS = 9;
void startRead(uint16_t addr) {
  setPin(CS,LOW);
  setPin(CS,HIGH);
  doBit(1); // start bit
  doBit(1); // read op 0
  doBit(0); // read op 1
  doBit(0); // don't care
  for (int i = 0; i < ADDR_BITS; i++) {
    int bit = (addr >> (ADDR_BITS-i)) & 0x01;
    doBit(bit);
  }
}  

void endRead() {
  setPin(CS,LOW);
}

uint16_t readWord() {
  uint16_t data = 0;
  for (int i = 0; i < 16; i++) {
    data = data << 1;
    data = data | ((doBit(0) == HIGH)?1:0);
  }
  return data;
}

void loop() {
  delay(5000);
  startRead(0);
  for (int i = 0; i < 512; i++) {
    uint16_t w = readWord();
    Serial.write((w>>8) & 0xff);
    Serial.write(w & 0xff);
  }
  endRead();
  while(1);
}
