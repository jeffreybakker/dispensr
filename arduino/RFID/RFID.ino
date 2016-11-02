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

unsigned char *KEY = (unsigned char *) "ZxPEh7ezUDq54pRv";

#define MOD_ADLER 65521

#define PROTOCOL_VERSION 0x01

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

MFRC522 mfrc522(SS_PIN, RST_PIN);	// Create MFRC522 instance.

byte lcnt = 0;
byte rcnt = 0;

STATE state = STATE_RESET;

uint32_t adler32(unsigned char *data, uint8_t len) {
  uint32_t a = 1, b = 0;
  uint8_t index;
  
  /* Process each byte of the data in order */
  for (index = 0; index < len; ++index)
  {
      a = (a + data[index]) % MOD_ADLER;
      b = (b + a) % MOD_ADLER;
  }
  
  return ((b << 16) | a);
}

uint32_t hmac(unsigned char *data, uint8_t len) {
  unsigned char buf[260];
  uint32_t key = adler32(KEY, 16); // Assume the length(key) > 4
  uint32_t o_key_pad = 0x5C5C5C5C ^ key;
  uint32_t i_key_pad = 0x36363636 ^ key;

  buf[0] = (i_key_pad >> 24) & 0xFF;
  buf[1] = (i_key_pad >> 16) & 0xFF;
  buf[2] = (i_key_pad >>  8) & 0xFF;
  buf[3] = (i_key_pad >>  0) & 0xFF;

  for (int i=0; i<len; ++i) {
    buf[4+i] = data[i];
  }

  uint32_t hash = adler32(buf, len + 4);

  buf[0] = (o_key_pad >> 24) & 0xFF;
  buf[1] = (o_key_pad >> 16) & 0xFF;
  buf[2] = (o_key_pad >>  8) & 0xFF;
  buf[3] = (o_key_pad >>  0) & 0xFF;
  
  buf[4] = (hash >> 24) & 0xFF;
  buf[5] = (hash >> 16) & 0xFF;
  buf[6] = (hash >>  8) & 0xFF;
  buf[7] = (hash >>  0) & 0xFF;

  return adler32(buf, 8);
}

void encrypt(unsigned char *data, uint8_t len) {
  for (int i=0; i<len; ++i) {
    data[i] ^= KEY[i % 16];
  }
}

void decrypt(unsigned char *data, uint8_t len) {
  for (int i=0; i<len; ++i) {
    data[i] ^= KEY[i % 16];
  }
}

void setup() {
	Serial.begin(9600);	// Initialize serial communications with the PC
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();	// Init MFRC522 card

  Serial.setTimeout(5000);

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

  unsigned char buf[128];

  buf[0] = PROTOCOL_VERSION;
  buf[1] = lcnt; // Local counter
  buf[2] = 6; // Data length
  buf[3] = OP_READ;
  buf[4] = 4; // Value length
  buf[5] = mfrc522.uid.uidByte[0];
  buf[6] = mfrc522.uid.uidByte[1];
  buf[7] = mfrc522.uid.uidByte[2];
  buf[8] = mfrc522.uid.uidByte[3];

  encrypt(&buf[3], 6);

  uint32_t sig = hmac(buf, 9);

  buf[9]  = (sig >> 24) & 0xFF;
  buf[10] = (sig >> 16) & 0xFF;
  buf[11] = (sig >>  8) & 0xFF;
  buf[12] = (sig >>  0) & 0xFF;

  byte len = 13;

  for (int i=0; i<len; ++i) {
    Serial.print((char) buf[i]);
  }

  state = STATE_WAIT_AUTH;
  //delay(1000);
}

void s_wait_auth() {
  if (Serial.available() < 3) {
    return;
  }
  
  unsigned char buf[260];
  Serial.readBytes(buf, 3);
  Serial.readBytes(&buf[3], buf[2] + 4);

  byte len = 3 + buf[2];

  uint32_t signature = buf[len];
  signature = (signature << 8) | buf[len+1];
  signature = (signature << 8) | buf[len+2];
  signature = (signature << 8) | buf[len+3];
  
  uint32_t verify = hmac(buf, len);

  // Invalid signature
  if (signature != verify) {
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    delay(150);
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    delay(150);
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    delay(150);
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    delay(150);
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    delay(150);
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    
    state = STATE_RESET;
    
    return;
  }

  decrypt(&buf[3], buf[2]);
  
  switch(buf[3]) {
    case OP_ACCEPT:
      state = STATE_ACCEPT;
      break;
    case OP_REJECT:
      state = STATE_REJECT;
      break;
    default:
      state = STATE_RESET;
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
      state = STATE_RESET;
	}
}

