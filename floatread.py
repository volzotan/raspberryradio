import struct
import os

FILENAME = "testdata_44kHz.dat"

fd = open(FILENAME)

# get filesize
# one float = 4 Byte
statinfo = os.stat(FILENAME)
n = statinfo.st_size/4

floats = struct.unpack('f'*n, fd.read(4*n))

print(max(floats))
print(n/44100)