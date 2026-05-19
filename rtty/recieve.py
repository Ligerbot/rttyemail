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
#credit to imaoca on github for the decoder that I modified: https://github.com/imaoca/RTTY/

smp= 44100          # Sampling Rate
FQm= smp/1575.0     # Mark Frequency 914Hz
FQs= smp/2425.0    # Space Frequency 1086Hz
#wind= int(smp / 75)           # windows size Integer was 32
wind= 32           # windows size Integer was 32

#claude helped with this part
q = queue.Queue()
def callback(indata, frames, time, status):
    q.put(indata[:, 0].copy())

class FakeBuf:
    def readframes(self, n):
        chunk = q.get()
        # convert float32 [-1,1] to uint8 [0,255] to match original buf[0]-128
        return ((chunk * 128) + 128).astype(np.uint8)
    def getnframes(self):
        return 999999999

#following code was somewhat copied from https://python-sounddevice.readthedocs.io/en/0.3.12/usage.html#callback-streams
duration = 99999999999999999999999999999
#def callback(indata, outdata, frames, time):
#	global wav
#	wav = indata[:, 0]
#	print(str(indata[:, 0]))
chunks = []

def callback2(indata, frames, time, status):
    chunks.append(indata[:, 0].copy())

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
decodedemail = ""
block = []
bits = []
bit_pos = 0
mode = 0
SAMPLES_PER_BIT = int(smp / 75)
def decode(waveFile):
	global decodedemail, bits, mode, bit_pos
	global block
	for j in range(waveFile.getnframes()):
		buf = waveFile.readframes(1)
		block.append(float(buf[0] - 128))

		if len(block) >= SAMPLES_PER_BIT:
			t = np.arange(len(block)) / smp
			mk = np.abs(np.sum(np.array(block) * np.exp(-2j * np.pi * 1575 * t)))
			sp = np.abs(np.sum(np.array(block) * np.exp(-2j * np.pi * 2425 * t)))
			bits.append(1 if mk > sp else 0)
			block = []
			while bit_pos < len(bits) - 8:
				if bits[bit_pos] == 1 and bits[bit_pos+1] == 0:
					frame = bits[bit_pos+2:bit_pos+7]
					code = ''.join(str(b) for b in frame)
#					\if code == '11111':
#						mode = 0
#					elif code == '11011':
#						mode = 1
#					else:
					char = baudot.decode_baudot(frame)
					if char:
						decodedemail += char
						if char == '\r':
							char = '\n'
						print(char, end='', flush=True)
						if "---END  RTTY  EMAIL---" in decodedemail:
							toEmail(decodedemail)
							decodedemail = ""
						if "---START  RTTY  EMAIL---" in decodedemail:
							decodedemail = decodedemail.strip("---START  RTTY  EMAIL---")
							print("Receiving possible email now")
						if "-SSTV  SIGNAL  ATTACHED-" in decodedemail:
							stream = sd.InputStream(samplerate=44100, channels=1, dtype='float32', callback=callback2)
							stream.start()
							print("Listening for SSTV signal. If there is none, restart program and try recieving again.")
							time.sleep(40)
							stream.stop()
							audio = np.concatenate(chunks)
							sf.write('local_libraries/output.wav', audio, 44100)
							mysstv.decode()
							print("Check for attachment.png in the working directory")

					bit_pos += 8
				else:
					bit_pos += 1

	waveFile.close()

with sd.InputStream(samplerate=44100, channels=2, dtype='float32', blocksize=1, callback=callback):
	waveFile = FakeBuf()
	decode(waveFile)
#	sd.sleep(int(duration * 1000))
