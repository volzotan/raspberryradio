import sys
import struct

fd = open("testdata_new_44kHz.dat")
preamble = False
pointer = 0
liste = [1,1,3,1,1,1]


def read_signal():
	
	haveAlreadyFoundAHill = False
	
	hillcounter = 0
	valleycounter = 0
	
	while(True):
		value = struct.unpack('h', fd.read(2))
		value = value[0]
		
		if haveAlreadyFoundAHill == False:

			if(value>=2000):
				hill = True
				haveAlreadyFoundAHill = True

		else:
			if hill:
				if(value>=2000):
					hillcounter += 1
				else:
					hill = False
			else:
				if (value >=2000):
					return((hillcounter, valleycounter))
				else:
					valleycounter += 1
				

try:
	while True:
		print ("hill: " + str(read_signal()[0] / 15))
		print ("valley: " + str(read_signal()[1] / 15))
		#print(read_signal())
	
except Exception as e:
	print(e)

def translate(value, counter=1):
	if(value%15 > 3):
		return -1
	else:
		if(value-15 <= 3):
			return counter
		else:
			if(value-15 >15):
				return translate(value-15, counter+1)
	

def checkPreamble():
	try:
		while True:
			temp = read_signal()
			hill = translate(temp[0])
			valley = translate(temp[1])
			if(hill != -1 and valley != -1):
				for i in range(0, len(list), 2):
					if not vergleich(hill, i) and not vergleich(valley, i+1):
						return False
	except Exception as e:
		print(e)
	return True

		
		
def vergleich(value, counter):
	if(value == liste[counter]):
		return True
	else:
		return False
		
		
print(checkPreamble())
