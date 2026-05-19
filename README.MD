# RTTY Email

This is two python programs that recieve and send emails using a ham radio digital mode called RTTY. If you followed the bit.ly link sent in morse code after a transmission, feel free to send an email or just recieve. Instructions to run these programs are included below.

Note: This isn't error tolerant at all. If a bit gets flipped it won't fix it. Don't expect it to work unless you have a good signal and no noise or anything messing up the reciever.

Also, depending on where you are, you may legally be required to to let it do the morse transmission afterwards so people can get access to the decoder and use it too.

## How to run it

The program for recieving uses a lot of local libraries included in this repo. Those should work no problem. You may need to run the following to install all other libraries though:

```pip3 install numpy sounddevice soundfile --break-system-packages``` *

Then run `python3 recieve.py` or `python3 sendmail.py` depending on what you want to do. Be sure not to interrupt any nets or anything with this obviously because people won't like you (RTTY is very annoying).

* The option `--break-system-packages` is required for me (Debian 13). May not be required for other enviroments.

## Still to do

Make it remember your callsign

Contacts list?

Integrate it with Thunderbird?

Error Correction?

GUI or TUI

Selective Email Reception (Only showing emails addressed to your callsign)

SnackMail email address that forwards emails from ham radio to internet (would require a base station connected to a computer that is always on).

Email me (ilan@snackmail.cc) if you have any ideas.

Play image attachments using SSTV?
