import email
import local_libraries.baudot as baudot
import os
import wave
import numpy as np
import sounddevice as sd
import queue
#credit to imaoca on github for the decoder that I modified: https://github.com/imaoca/RTTY/

smp= 44100          # Sampling Rate
FQm= smp/1575.0     # Mark Frequency 914Hz
FQs= smp/2425.0    # Space Frequency 1086Hz
wind= 32           # windows size Integer

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
def decode(waveFile):
	decodedemail = []
	fivebitbytethingy = []
	in_frame = False
	frame_bits = []
	SAMPLES_PER_BIT = int(smp / 75)
	sample_count = 0
	mq=[];mi=[];sq=[];si=[]
	for j in range(waveFile.getnframes()):
		buf = waveFile.readframes(1)
		mq.append((buf[0]-128)*np.sin(np.pi*2.0/FQm*j))
		mi.append((buf[0]-128)*np.cos(np.pi*2.0/FQm*j))
		sq.append((buf[0]-128)*np.sin(np.pi*2.0/FQs*j))
		si.append((buf[0]-128)*np.cos(np.pi*2.0/FQs*j))
		mk = np.sqrt(sum(mq)**2 + sum(mi)**2)
		sp = np.sqrt(sum(sq)**2 + sum(si)**2)
#		print(mk,sp,int(mk>sp),sep=",")
#		print(int(mk>sp),sep=",", end="")
#		if len(fivebitbytethingy) >= 5:
#			#print(fivebitbytethingy)
#			print(baudot.decode_baudot(fivebitbytethingy), end="")
#			fivebitbytethingy = []
#		else:
#			fivebitbytethingy.append(int(mk>sp))

		#claude helped make this section and I modifed it a bit
		bit = int(mk > sp)
		sample_count += 1
		if sample_count >= SAMPLES_PER_BIT:
			sample_count = 0
			if not in_frame:
				if bit == 0:
					in_frame = True
					frame_bits = []
			else:
				frame_bits.append(bit)
				if len(frame_bits) == 5:
					char = baudot.decode_baudot(frame_bits)
					if char:
#						if char == "\n":
#							end = "\n"
#						else:
#							end = ""
						decodedemail = str(decodedemail) + str(char)
						print(char, end = "", flush=True)
						if "---END  RTTY  EMAIL---" in decodedemail:
							toEmail(decodedemail)
							decodedemail = []
						else:
							pass
						if "---START  RTTY  EMAIL---" in decodedemail:
							decodedemail = decodedemail.strip("---START  RTTY  EMAIL---")
							print("Recieving possible email now")
					in_frame = False
					frame_bits = []
		if j>wind:
			mq.pop(0);mi.pop(0);sq.pop(0);si.pop(0)
	waveFile.close()

with sd.InputStream(samplerate=44100, channels=2, dtype='float32', blocksize=1, callback=callback):
	waveFile = FakeBuf()
	decode(waveFile)
#	sd.sleep(int(duration * 1000))
