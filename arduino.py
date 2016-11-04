#!/usr/bin/env python3

from binascii import hexlify
from struct import pack, unpack
import serial


class Interface(object):
    """ The communication interface for the RFID reader """

    VERSION = 0x01

    # Protocol opcodes
    OP_READ = 0x00
    OP_ACCEPT = 0x01
    OP_REJECT = 0x02
    OP_RESET = 0xFF

    MOD_ADLER = 65521

    def __init__(self, key, port='/dev/ttyACM0'):
        # Reset the packet counters
        self._lcount = 0
        self._rcount = 0

        # Set the secret key
        self._key = key

        # Open the serial port
        self._serial = serial.Serial(port)

    def adler32(self, buf):
        """ Compute the Adler-32 hash of a bytestring """

        a, b = 1, 0
        for i in range(len(buf)):
            a = (a + buf[i]) % self.MOD_ADLER
            b = (b + a) % self.MOD_ADLER
    
        val = (b << 16) | a

        return bytes(pack('!I', val))

    def hmac(self, msg):
        """ Compute the HMAC-Adler-32 of a bytestring """

        key = self._key

        # If the key is longer than the block size, take the hash
        if len(key) > 4:
            key = self.adler32(key)

        # If the key is shorter, pad with zeroes
        if len(key) < 4:
            key = key + bytes(4 - len(key))

        # Calculate the `o_key_pad` and `i_key_pad`
        o_key_pad = bytes([0x5c ^ i for i in key])
        i_key_pad = bytes([0x36 ^ i for i in key])

        return self.adler32(o_key_pad + self.adler32(i_key_pad + msg))
    
    def encrypt(self, msg):
        """ Encrypt a message by XOR'ing the key """

        klen = len(self._key)
        mlen = len(msg)
        return bytes([msg[i] ^ self._key[i % klen] for i in range(mlen)])

    def decrypt(self, msg):
        """ Decrypt a message by XOR'ing the key """
        return self.encrypt(msg)

    def pack(self, msg):
        """ Encode and encrypt a packet """

        data = bytes([self.VERSION, self._lcount, len(msg)])
        data += self.encrypt(msg)
        data += self.hmac(data)

        return data

    def unpack(self, data):
        """ Decode and decrypt a packet """

        # Decode the protocol parameters
        version = data[0]
        count = data[1]
        length = data[2]
        msg = self.decrypt(data[3:3+length])
        hmac = data[3+length:]

        # Unknown version/header, raise an exception
        if version != 1:
            raise Exception('Unknown protocol version: {}'.format(version))

        # Verify the HMAC
        verify = self.hmac(data[:-4])
        if verify != hmac:
            raise Exception('Invalid HMAC signature')

        return msg

    def read_rfid(self):
        """ Make a blocking call to read an RFID card """

        # Read the packet from the serial port
        hdr = self._serial.read(3)
        payload = self._serial.read(hdr[2] + 4)

        # Decode the message
        msg = self.unpack(hdr + payload)

        if msg[0] != self.OP_READ:
            raise Exception('Invalid opcode: {}'.format(msg[0]))

        # Convert the UID to an int
        uid, = unpack('!I', msg[2:])

        return uid

    def send_accept(self):
        """ Send an ACCEPT opcode to the Arduino """
        data = self.pack(bytes([self.OP_ACCEPT]))
        self._serial.write(data)

    def send_reject(self):
        """ Send a REJECT opcode to the Arduino """
        data = self.pack(bytes([self.OP_REJECT]))
        self._serial.write(data)

if __name__ == '__main__':
    key = b'ZxPEh7ezUDq54pRv'
    # key = b'Testing123'

    ard = Interface(key)
    
    while True:
        uid = ard.read_rfid()
        print(uid)

        if uid == 586812701:
            ard.send_accept()
        else:
            ard.send_reject()

