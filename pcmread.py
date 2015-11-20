import struct
import os

FILENAME = "testdata_44kHz.dat"

fd = open(FILENAME)

# get filesize
# one signed 16bit integer = 2 Byte
statinfo = os.stat(FILENAME)
n = statinfo.st_size/2

values = struct.unpack('h'*n, fd.read(2*n))
print(max(values))

