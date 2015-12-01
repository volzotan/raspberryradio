import sys
import struct

class Reader(object):

	fd = open("testdata_new_44kHz.dat")
	fd = sys.stdin
	preamble = False
	pointer = 0
	liste = [1,1,3,1,1,1]
	
	
	def read_signal(self):
		
		haveAlreadyFoundAHill = False
		
		hillcounter = 0
		valleycounter = 0
		
		while(True):
			try:
				value = struct.unpack('h', self.fd.read(2))
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
			except Exception as e:
				sys.stdout.write("\n")
				sys.exit(-1)
					
	def translate(self, value, counter=1):
		if(value>=15):
			if(value%15 > 5):
				return -1
			else:
				if(value-15 <= 5):
					return counter
				else:
					if(value-15 >=15):
						return self.translate(value-15, counter+1)
		else:
			if(value-15 > 5):
				return -1
			else:
				if(value-15 <= 5):
					return counter
				else:
					if(value-15 >15):
						return self.translate(value-15, counter+1)

		
	
	def checkPreamble(self):
		try:
			while True:
				for i in range(0, len(self.liste), 2):
					temp = self.read_signal()
					hill = self.translate(temp[0])
					valley = self.translate(temp[1])
					if self.vergleich(hill,i) and self.vergleich(valley,i+1):
						if(i == len(self.liste)-2):
							return True
						else:
							continue
					else:
						break
		except Exception as e:
			return False
	
			
			
	def vergleich(self, value, counter):
		if(value == self.liste[counter]):
			return True
		else:
			return False
	
	def getBytes(self, hill, valley):
		if hill == 2 and valley == 3:
			return 0
		else:
			if hill == 4 and valley == 1:
				return 1
			else:
				return -1	

if __name__ == "__main__":
	reader = Reader()
	array = [None] * 8
	exponent = 0
	num = 0
	
	try:
		while True:
			if reader.checkPreamble():
				for i in range (0, len(array)):
					temp = reader.read_signal()
					hill = reader.translate(temp[0])
					valley = reader.translate(temp[1])
					if reader.getBytes(hill, valley) != -1:
						array[i] = reader.getBytes(hill,valley)
					else:
						print("Sorry, can't read your signal :(")
				for elem in array:
					#print array
					#print((num, elem, exponent))
					num = num + (elem * (2 ** exponent))
					#print(num),
					exponent = exponent +1
				sys.stdout.write(str(unichr(num)))
				num = 0
				exponent = 0
	except Exception as e:
		pass
