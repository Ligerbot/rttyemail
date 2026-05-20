import base64
import subprocess
import reedsolo #reed solomon error correction
import local_libraries.fskmodem as fskmodem
import time
import local_libraries.mysstv as mysstv #not pysstv, MY sstv!
import email
import os
import soundfile as sf
import sounddevice as sd
import queue

modem = fskmodem.Modem(baudrate=125, confidence = 0.1, sync_byte= '0x23', start=False)
#rsc = reedsolo.RSCodec(20, c_exp=7)
rsc = reedsolo.RSCodec(50)
#modem.MTU = 10000

def listenforemail():
	global char
	global proc
	proc = subprocess.Popen(
		['minimodem', '--rx', '300', '--confidence', '0.1', '--sync-byte', '0x23', '-q', '--binary-output'],
		stdout=subprocess.PIPE,
		stderr=subprocess.DEVNULL
	)
	char = b""
	while not b"!<" in char:
#		char = char + proc.stdout.read(1) #.decode("utf-8", errors="replace"))

		#claude helped with the following two lines
		bits = proc.stdout.read(9).strip()  # 8 bits + newline
		char = char + bytes([int(bits[::-1], 2)])

		if b"!>" in char:
			print("\033[92m" + "Recieving Potential Email" + "\033[0m")
			char = b""
#	print("Email before Reed-Solomon error correction: \n" + str(char.decode("utf-8", errors="replace")))
	proc.terminate() #clean up
#	print(str(char))
#	char = char.decode("utf-8", errors="replace").encode("utf-8")
#	print(str(char))
	stripped = char.replace(b"!<", b"").replace(b"!>", b"")
	doubletrouble = stripped.split(b"<b64 parity start>")
	text = doubletrouble[0]
	parity = base64.b64decode(doubletrouble[1])
	full = text + parity
#	print(stripped.decode("utf-8", errors="ignore"))
#	print(stripped)
	fixed = rsc.decode(full)[0]
	print("\033[92m" + "Recieved an email and corrected any errors" + "\033[0m")
	print(str(fixed.decode("utf-8")))
#	print(str(fixed.decode("utf-8")))
try:
	while True:
		listenforemail()
except reedsolo.ReedSolomonError as e:
	print("\033[91m" + "Unable to correct recieved email. Printing out what was possible to decode:" + "\033[0m")
	print(str(char.decode("utf-8", errors="replace")))
finally:
	print("Killing off minimodem")
	proc.terminate()
