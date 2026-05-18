import fskmodem
import time
import local_libraries.mysstv as mysstv #not pysstv, MY sstv!
import email
import local_libraries.baudot as baudot
import os
import wave
import numpy as np
import soundfile as sf
import sounddevice as sd
import queue

modem = fskmodem.Modem(baudrate=1200, start=False)

def callback(sounddataa):
	decoded = sounddataa.decode("utf-8")
	print("Debug output: " + decoded)
	if "-SSTV  SIGNAL  ATTACHED-" in decoded:
		#to be implemented
		pass

	toEmail(decoded)

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
