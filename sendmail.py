import numpy as np
#import pysstv.color as pysstv
#import PIL
#import PIL.Image
import sounddevice as sd
import soundfile as sf
import local_libraries.pyrtty as pyrtty
from email.message import EmailMessage
import email.utils
import time

msg = EmailMessage()

print("Composing RTTY email")
msg['From'] = input("Callsign: ")
msg['To'] = input("Callsign to send email too: ")
msg['Subject'] = input("Subject: ")
msg['Date'] = email.utils.formatdate(localtime=True)
#msg['Message-ID'] = email.utils.make_msgid(domain='example.com')
body = input("Message Body: ")
msg.set_payload(body)

attachments = input("Do you want to attach an image? (y/n): ")
attachmentdata = ""
if attachments == "y":
	location = input("Enter path to image: ")
	image = PIL.Image.open(location)
	target = (320, 240)
	image.thumbnail(target, PIL.Image.LANCZOS)
	newimage = PIL.Image.new("RGB", target)
	box = ((target[0] - image.size[0]) // 2, (target[1] - image.size[1]) // 2)
	newimage.paste(image, box)
	image = newimage
	prompts = input("Show image(y/n)? ")
	if prompts == "y":
		image.show()
	converted = pysstv.Robot36(image, 44100, 16)
	samples = list(converted.gen_samples())
	sstv = np.array(samples, dtype=np.int16)
	attachmentdata = "---SSTV SIGNAL ATTACHED---"
email = "---START RTTY EMAIL---\n---START RTTY EMAIL---\n" + msg.as_string() + "\n---END RTTY EMAIL---\n---END RTTY EMAIL---\n" + attachmentdata
print("Sending the following email over RTTY now: \n" + email)
#print(msg.as_string())
baudot = pyrtty.text_to_baudot(email)
signal = pyrtty.baudot_to_afsk(baudot)
pyrtty.play_afsk_signal(signal)
time.sleep(0.5)
if attachments == "y":
	print("Playing SSTV now")
	sd.play(sstv, 44100)
	sd.wait()
print("Playing morse code with link to github. May be required by law to show how it works so people can decode it")
data, samplerate = sf.read('protocol_specifications_link.wav')
sd.play(data, samplerate)
sd.wait()
