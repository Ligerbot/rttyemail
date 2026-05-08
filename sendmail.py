import local_libraries.pyrtty
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
msg.set_content(body)
email = "---START RTTY EMAIL---\n" + msg.as_string() + "\n---END RTTY EMAIL---"
print("Sending the following email over RTTY now: \n" + email)
#print(msg.as_string())
baudot = pyrtty.text_to_baudot(email)
signal = pyrtty.baudot_to_afsk(baudot)
pyrtty.play_afsk_signal(signal)
