#include <stdint.h>

// Set MAX_ADDR to the largest address you need
// to read. For example, for the 27C512 chips,
// you'll want to use a MAX_ADDR of 65536.
// (That's 512 * 1024 / 8.)
// A 27C256 would be 256 kilobits, or 256 * 1024 / 8 =
// 32768.
#define MAX_ADDR 65536L

// On my board, I've connected pins 26-41
// to the A0-A15 lines, and pins 2-10 to the
// Q0-Q7 lines. You'll want to change these
// pin choices to match your setup.
#define A0 26
#define Q0 2

// When you're all wired up, hit the reset button
// to start dumping the hex codes.

void setup() {
  for (int i = A0; i < A0+16; i++) {
    digitalWrite(i,LOW);
    pinMode(i, OUTPUT);
  }
  for (int i = Q0; i < Q0+8; i++) {
    digitalWrite(i,HIGH);
    pinMode(i, INPUT);
  }
  Serial.begin(115200);
}

void writeAddr(uint32_t addr) {
  uint32_t mask = 0x01;
  for (int i = A0; i < A0+16; i++) {
    if ((mask & addr) != 0) {
      digitalWrite(i,HIGH);
    } else { 
      digitalWrite(i,LOW);
    }
    mask = mask << 1;
  }
}


uint8_t readByte() {
  uint8_t data = 0;
  uint8_t mask = 0x1;
  for (int i = Q0; i < Q0+8; i++) {
    if (digitalRead(i) == HIGH) {
      data |= mask;
    }
    mask = mask << 1;
  }
  return data;
}

void loop() {
  uint32_t addr = 0;
  while (addr < MAX_ADDR) {
    for (int i = 0; i < 16; i++) {
      writeAddr(addr);
      uint8_t b = readByte();
      Serial.print(b, HEX);
      Serial.print(" ");
      addr++;
    }
    Serial.println("");
  }
  while (1) {}
}
