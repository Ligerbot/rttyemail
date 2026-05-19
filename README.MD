# RTTY Email

This is two python programs that recieve and send emails using FSK (Frequency Shift Keying). If you followed the bit.ly link sent in morse code after a transmission over the air, an email over the air would be appreciated.

Note: This isn't error tolerant at all. If a bit gets flipped it won't fix it. Don't expect it to work unless you have a good signal and no noise or anything messing up the reciever.

It is a good practice to let anyone listening in on your transmission be able to decode it too, so it is recomended to let it play the morse code after sending an email so that anyone listening can run this themselves.

## How to run it

You **will** need the software `minimodem`. On Debian 13 you can just run `sudo apt install minimodem`, but it depends on your operating system.

Then run `python3 recieve.py` or `python3 sendmail.py` depending on what you want to do. Be sure not to interrupt any nets or anything with this obviously because people definetly won't like you.

## Still to do

* Make it remember your callsign

* Contacts list?

* Integrate it with Thunderbird

* Error Correction

* GUI or TUI

* Selective Email Reception (Only showing emails addressed to your callsign)

* SnackMail email address that forwards emails from ham radio to internet (would require a base station connected to a computer that is always on).

* Play image attachments using SSTV?

Email me (ilan@snackmail.cc) if you have any ideas.

