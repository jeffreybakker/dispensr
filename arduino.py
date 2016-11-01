import serial

MOD_ADLER = 65521


def adler32(buf):
    a, b = 1, 0
    for c in buf:
        a = (a + ord(c)) % MOD_ADLER
        b = (b + a) % MOD_ADLER;

    return (b << 16) | a


KEY = "ZxPEh7ezUDq54pRv"

OPCODE_READ = 0x00
OPCODE_ACCEPT = 0x01
OPCODE_REJECT = 0x02
OPCODE_RESET = 0xFF

ser = serial.Serial('/dev/ttyACM0')

# Reset the remote device
ser.write(chr(OPCODE_RESET))


def readUID():
    header = ord(ser.read())
    if header != 0x55:
        raise Exception('invalid protocol header')

    l = ord(ser.read())

    data = ser.read(l)
    buf = ''

    for i in range(l):
        buf += chr(ord(data[i]) ^ ord(KEY[i % 16]))

    t = ord(buf[0])
    l = ord(buf[1])
    v = buf[2:2 + l].encode('hex')
    cksum = buf[2 + l:]

    verify = adler32(buf[:-4])

    print(buf[:-4].encode('hex'))

    print(cksum.encode('hex'), verify)

    if t == OPCODE_READ:
        print('Read card:', v, )

        if v == '22fa0d1d':
            print('Accept')
            ser.write(chr(OPCODE_ACCEPT))
        else:
            print('Reject')
            ser.write(chr(OPCODE_REJECT))
    else:
        print('Unknown opcode:', t)
