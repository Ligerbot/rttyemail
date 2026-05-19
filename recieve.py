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
rsc = reedsolo.RSCodec(20, c_exp=7)
#modem.MTU = 10000

def listenforemail():
	global proc
	proc = subprocess.Popen(
		['minimodem', '--rx', '300', '--confidence', '0.1', '--sync-byte', '0x23', '-q'],
		stdout=subprocess.PIPE,
		stderr=subprocess.DEVNULL
	)
	char = b""
	while not b"!<" in char:
		char = char + proc.stdout.read(1) #.decode("utf-8", errors="replace"))
		if b"!>" in char:
			print("Recieving Frame")
			char = b""
	proc.terminate() #clean up
	print(str(char))
	char = char.decode("utf-8", errors="backslashreplace").encode("utf-8")
	print(str(char))
	stripped = char.replace(b"!<", b"").replace(b">!", b"")
	print(stripped.decode("utf-8", errors="ignore"))
	fixed = rsc.decode(stripped)[0]
	print("Fixed: " + str(fixed).decode("utf-8"))
#	print(str(fixed.decode("utf-8")))
try:
	listenforemail()
finally:
	print("Killing off minimodem")
	proc.terminate()
def callback(sounddataa):
	sounddataa = sounddataa.lstrip(b'\x23')
	unhexed = bytes.fromhex(sounddataa.decode("utf-8"))
	print(unhexed)
	corrected = rsc.decode(unhexed)[0].decode("utf-8")
	print("Debug output: " + corrected)
	if "-SSTV  SIGNAL  ATTACHED-" in corrected:
		#to be implemented, low priority
		pass

	toEmail(corrected)

def toEmail(text):
	decodedeml = email.message_from_string(text)
	msg = decodedeml
	print("\n")
	print("\n")
	print("Recieved the following email:")
	print(msg['From'])
	print(msg['To'])
	print(msg['Subject'])
	print(msg.get_payload())
	print("Done decoding email")
decoded = modem.set_rx_callback(callback)
modem.start()
print("Waiting for email to be sent")
while True:
	#keep the decoder alive
	time.sleep(1)


#keeping for when I re  add the sstv decoder.
#
#						print(char, end='', flush=True)
#						if "---END  RTTY  EMAIL---" in decodedemail:
#							toEmail(decodedemail)
#							decodedemail = ""
#						if "---START  RTTY  EMAIL---" in decodedemail:
#							decodedemail = decodedemail.strip("---START  RTTY  EMAIL---")
#							print("Receiving possible email now")
#						if "-SSTV  SIGNAL  ATTACHED-" in decodedemail:
#							stream = sd.InputStream(samplerate=44100, channels=1, dtype='float32', callback=callback2)
#							stream.start()
#							print("Listening for SSTV signal. If there is none, restart program and try recieving again.")
#							time.sleep(40)
#							stream.stop()
#							audio = np.concatenate(chunks)
#							sf.write('local_libraries/output.wav', audio, 44100)
#							mysstv.decode()
#							print("Check for attachment.png in the working directory")
#
#					bit_pos += 8
#				else:
#					bit_pos += 1
#
#	waveFile.close()
