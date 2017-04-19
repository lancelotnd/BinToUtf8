# -*- coding: utf-8 -*-
# A simple python version of http://robbi-985.homeip.net/information/bintoutf8_pseudo.txt
import os,codecs,unicodedata,sys
import cPickle as pickle
err = 0
BCLHighestUsed = -1
BCLByte = [0] * 256
BCLCharCode = [0] * 256

def gbl():
	if os.name == 'posix':
		sys.stdout.write("\033[F")
	else:
		return #no pretty things for you windows

def SaveBCL():
	global BCLHighestUsed,BCLByte,BCLCharCode
	save = { "byte" : BCLByte, "charcode":BCLCharCode }
	pickle.dump(save, open( "save.bcl", "wb"))

def LoadBCL():
	global BCLHighestUsed,BCLByte,BCLCharCode
	save = pickle.load(open("save.bcl", "rb"))
	BCLByte = save["byte"]
	BCLCharCode = save["charcode"]

def ConvBinToUTF8(inp, out):
	global BCLHighestUsed,BCLByte,BCLCharCode
	BCLInit()
	with open(inp, 'rb') as fi:
		AllBin = fi.read()
		sizeinput = len(AllBin)

	with codecs.open(out, encoding='utf-8', mode='w') as fo:
		pos = 0
		for by in AllBin:
			#fo.write(struct.pack('i', ByteToCharCode(by)))
			#fo.write(str(ByteToCharCode(by)).encode("utf-8").decode("utf-8"))
			fo.write(unichr(ByteToCharCode(by)))
			if pos % 100 == 0:
					print str(int((float(pos)/float(sizeinput))*100))+"%","("+str(pos/1000)+"kb","/",str(sizeinput/1000)+"kb)"
					gbl()
			pos += 1
	print "Finished                       "
	SaveBCL()

def BCLInit():
	global BCLHighestUsed,BCLByte,BCLCharCode
	BCLHighestUsed = -1
	
	#This is where you set up BCLCharCode[], i.e. the character codes in the lookup table.
	#Values are your choice, but I did it this way:
	#LoopIndex = 0
	#Add ASCII characters:    #.../   0...9   :...@   A...Z   [...`   a...z   {...~
	for i in range(0x23,0x7E):
		BCLInitSingle(i)

	LoopIndex = 0

	while BCLHighestUsed < 255:
		BCLInitSingle(0x3900 + LoopIndex)
		LoopIndex += 1

	BCLHighestUsed = -1

def BCLInitSingle(NewCharCode):
	global BCLHighestUsed,BCLByte,BCLCharCode
	BCLHighestUsed += 1
	BCLCharCode[BCLHighestUsed] = NewCharCode

def ByteToCharCode(ByteVal):
	global BCLHighestUsed,BCLByte,BCLCharCode
	#Search for matching byte in lookup table and return the character code.
	CheckIndex = 0
	while CheckIndex <= BCLHighestUsed:
		if (BCLByte[CheckIndex] == ByteVal):
			return BCLCharCode[CheckIndex]
		CheckIndex += 1

	#None existed - add new entry for this byte, using next available character code.
	if (BCLHighestUsed < 255):
		BCLHighestUsed += 1
		BCLByte[BCLHighestUsed] = ByteVal
		return BCLCharCode[BCLHighestUsed]
	else:
		print "Ya done goofed"
		#There must be a bug somewhere - all 256 lookup entries are already used.

def ConvUTF8ToBin(inp, out):
	global BCLHighestUsed,BCLByte,BCLCharCode,err
	LoadBCL()							#Load previous lookup table arrays from ".bcl" file.
	with codecs.open(inp, encoding='utf-8', mode='r') as fi:	#A UTF-8-encoded text file.
		AllUTF8 = fi.read()
		sizeinput = len(AllUTF8)

	with open(out, 'wb') as fo:			#This will become a recreated file, e.g. raw 8-bit PCM data.
		pos = 0
		for i in AllUTF8:
			fo.write(BCLCharCodeToByte(i))
			if pos % 100 == 0:
					print str(int((float(pos)/float(sizeinput))*100))+"%","("+str(pos/1000)+"kb","/",str(sizeinput/1000)+"kb)"
					gbl()
			pos += 1
	print "Finished                       "
	print "Errors in conversion :", err

def BCLCharCodeToByte(CharCodeVal):
	global BCLHighestUsed,BCLByte,BCLCharCode,err
	#Search for matching character code in lookup table and return the byte.
	for CheckIndex in range(256):
		if (BCLCharCode[CheckIndex] == ord(CharCodeVal)):
			return BCLByte[CheckIndex]
	
	#IMPORTANT: Torch-rnn will write CR+LF at the end of its output, making text files 2
	#bytes longer than you requested of it. As CR and LF are not characters in our
	#lookup table (BCLCharCode[]), we will not have returned a value yet! You can choose
	#your own default value to return in this case here:
	return chr('\x00')
	err += 1
	
	#Not included in this pseudocode: I decided to keep track of the total number of these
	#mismatches and display an error at the end of conversion according to how many failed
	#(i.e. nothing serious if only 2 failed).

def usage():
	print "Usage:"
	print "	python utf8.py -e <input> <output> Encodes a file"
	print "	python utf8.py -d <input> <output> Decodes a file"

if len(sys.argv) <= 3:
	usage()
	exit()

if sys.argv[1] == "-e":
	ConvBinToUTF8(sys.argv[2],sys.argv[3])
elif sys.argv[1] == "-d":
	ConvUTF8ToBin(sys.argv[2],sys.argv[3])
else:
	usage()
	exit()
