import sounddevice as sd
import soundfile as sf
import local_libraries.pyrtty as pyrtty
from email.message import EmailMessage
import email.utils

msg = EmailMessage()

print("Composing RTTY email")
msg['From'] = input("Callsign: ")
msg['To'] = input("Callsign to send email too: ")
msg['Subject'] = input("Subject: ")
msg['Date'] = email.utils.formatdate(localtime=True)
#msg['Message-ID'] = email.utils.make_msgid(domain='example.com')
body = input("Message Body: ")
msg.set_payload(body)
email = "---START RTTY EMAIL---\n---START RTTY EMAIL---\n" + msg.as_string() + "\n---END RTTY EMAIL---\n---END RTTY EMAIL---\n"
print("Sending the following email over RTTY now: \n" + email)
#print(msg.as_string())
baudot = pyrtty.text_to_baudot(email)
signal = pyrtty.baudot_to_afsk(baudot)
pyrtty.play_afsk_signal(signal)
print("Playing morse code with link to github. May be required by law to show how it works so people can decode it")
data, samplerate = sf.read('protocol_specifications_link.wav')
sd.play(data, samplerate)
sd.wait()
