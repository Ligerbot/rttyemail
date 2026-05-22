import random
import curses
import re #regex is torture
import base64
import subprocess
import reedsolo #reed solomon error correction
import time
import local_libraries.mysstv as mysstv #not pysstv, MY sstv!
import email
import os
def init():
	global rsc
	if not os.path.exists("callsign.txt"):
	        callsign = input("Callsign: ")
	        with open("callsign.txt", "w") as g:
	                g.write(callsign)
	                g.close()
	else:
	        with open("callsign.txt", "r") as f:
	                callsign = f.read()
	                f.close()
#	print("Recieving emails as " + callsign)

#msg = EmailMessage()
#rsc = reedsolo.RSCodec(20, c_exp=7)
	rsc = reedsolo.RSCodec(70)
#modem.MTU = 10000
def dummyrecieve(stdscr):
	time.sleep(0.5)
	stdscr.addstr(1,0, "Recieving dummy email for testing")
	stdscr.refresh()
	time.sleep(1)
	stdscr.addstr(1,0,"                                     ")
	stdscr.refresh()
	randemail = f"To: {random.randint(0,10)}\nFrom: {random.randint(0,10)}\nSubject: {random.randint(0,10)}\nDate: {time.ctime()}\n\n{random.randint(10,100)}"
	return randemail

def listenforemail(stdscr):
	global plzwork
	global char
	global text
	global fixed
	global parity
	global proc
	try:
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
#				print("\033[92m" + "Recieving Potential Email" + "\033[0m")
				stdscr.addstr(1,0,"Recieving Potential Email")
				stdscr.refresh()
				char = b""
#			if key == 27 or key == ord("q"):
#				stdscr.addstr(1,0,"Exiting, one second...")
#				stdscr.refresh()
#				return "user-exit"
	#	print("Still alive")
	#	print("Email before Reed-Solomon error correction: \n" + str(char.decode("utf-8", errors="replace")))
		proc.terminate() #clean up
#	print(str(char.decode("utf-8",errors="replace")))
#	print(str(char))
#	char = char.decode("utf-8", errors="replace").encode("utf-8")
#	print(str(char))
		stripped = char.replace(b"!<", b"").replace(b"!>", b"").strip()
#	doubletrouble = stripped.split(b"<b64 parity>\n")
		doubletrouble = stripped.split(b"64>\n\n")
		text = doubletrouble[0]
		plzwork = re.sub(b'[^A-Za-z0-9+/=]', b'', doubletrouble[-1].strip())
		parity = base64.b64decode(plzwork, validate=False)
#	print(str(parity))
		full = text + parity
		stdscr.addstr(1,0,"                                     ")
		stdscr.refresh()
#	print(stripped.decode("utf-8", errors="ignore"))
#	print(stripped)
		fixed = rsc.decode(full)[0]
#		print("\033[92m" + "Recieved an email and corrected any errors" + "\033[0m")
#		print(str(fixed.decode("utf-8")))
		return str(fixed.decode("utf-8"))
#	print(str(fixed.decode("utf-8")))

	except reedsolo.ReedSolomonError as e:
		print("\033[91m" + "Unable to correct recieved email. Printing out what was possible to decode:" + "\033[0m")
#		print("I recieved this parity string: ")
#		print(str(plzwork))
#		print("The parity after being decoded from base 64: ")
#		print(str(parity))
#		print("I recieved this text: ")
#		print(str(text))
#		print(str(char.decode("utf-8", errors="replace")))
#	finally:
#		print("Killing off minimodem")
#		proc.terminate()
#		print("Stopping")
#		return "error"
