/*
 * Pin layout should be as follows:
 * Signal     Pin              Pin               Pin
 *            Arduino Uno      Arduino Mega      MFRC522 board
 * ------------------------------------------------------------
 * Reset      9                5                 RST
 * SPI SS     10               53                SDA
 * SPI MOSI   11               51                MOSI
 * SPI MISO   12               50                MISO
 * SPI SCK    13               52                SCK
 */

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

#define KEY "ZxPEh7ezUDq54pRv"

const int MOD_ADLER = 65521;

enum OPCODE : byte {
  OP_READ = 0x00,
  OP_ACCEPT = 0x01,
  OP_REJECT = 0x02,
  OP_RESET = 0xFF
};

enum STATE {
  STATE_READ,
  STATE_WAIT_AUTH,
  STATE_ACCEPT,
  STATE_REJECT,
  STATE_RESET,
};

union hash_t {
  uint32_t num;
  byte bytes[4];
};

MFRC522 mfrc522(SS_PIN, RST_PIN);	// Create MFRC522 instance.

STATE state = STATE_RESET;

hash_t adler32(char *data, size_t len) {
    uint32_t a = 1, b = 0;
    size_t index;
    
    /* Process each byte of the data in order */
    for (index = 0; index < len; ++index)
    {
        a = (a + data[index]) % MOD_ADLER;
        b = (b + a) % MOD_ADLER;
    }

    hash_t val;
    val.num = ((b << 16) | a);
    
    return val;
}

void setup() {
	Serial.begin(9600);	// Initialize serial communications with the PC
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();	// Init MFRC522 card

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
}

void s_read() {   
    if ( ! mfrc522.PICC_IsNewCardPresent()) {
      return;
    }
  
    // Select one of the cards
    if ( ! mfrc522.PICC_ReadCardSerial()) {
      return;
    }

  char buf[128];
  byte len = 6;

  buf[0] = 0x00;
  buf[1] = 4;
  buf[2] = mfrc522.uid.uidByte[0];
  buf[3] = mfrc522.uid.uidByte[1];
  buf[4] = mfrc522.uid.uidByte[2];
  buf[5] = mfrc522.uid.uidByte[3];

  hash_t hash = adler32(buf, len);

  buf[6] = hash.bytes[3];
  buf[7] = hash.bytes[2];
  buf[8] = hash.bytes[1];
  buf[9] = hash.bytes[0];

  len += 4;

  Serial.print((char) 0x55);
  Serial.print((char) len);

  for (int i = 0; i < len; ++i) {
    byte encrypt = ((byte) buf[i]) ^ KEY[i % 16];
    Serial.print((char) encrypt);
  }

  state = STATE_WAIT_AUTH;
}

void s_wait_auth() {
  if (Serial.available() == 0) {
    return;
  }
  
  byte t = Serial.read();
  
  switch(t) {
    case OP_ACCEPT:
      state = STATE_ACCEPT;
      break;
    case OP_REJECT:
      state = STATE_REJECT;
      break;
    case OP_RESET:
      state = STATE_RESET; 
      break;
  }
}

void s_accept() {
  digitalWrite(2, HIGH);
  delay(1000);
  digitalWrite(2, LOW);
  
  state = STATE_RESET;
}

void s_reject() {
  digitalWrite(3, HIGH);
  delay(1000);
  digitalWrite(3, LOW);

  state = STATE_RESET;
}

void s_reset() {
  // Clear the serial buffer
  while (Serial.available()) {
    Serial.read(); 
  }
  
  state = STATE_READ;
}

void loop() {
	switch(state) {
    case STATE_RESET:
      s_reset(); break;
    case STATE_READ:
      s_read(); break;
    case STATE_WAIT_AUTH:
      s_wait_auth(); break;
    case STATE_ACCEPT:
      s_accept(); break;
    case STATE_REJECT:
      s_reject(); break;
    default:
      state = STATE_READ;
	}
}

