# RTTY Email

This is two python programs that recieve and send emails using FSK (Frequency Shift Keying). If you followed the bit.ly link sent in morse code after a transmission over the air, an email over the air would be appreciated.

This is almost error tolerant. It can correct any errors besides ones that mess up the beginning and end.

It is a good practice to let anyone listening in on your transmission be able to decode it too, so it is recomended to let it play the morse code after sending an email so that anyone listening can run this themselves.

## How to run it

You **will** need the software `minimodem`. On Debian 13 you can just run `sudo apt install minimodem`, but it depends on your operating system.

Then run `python3 recieve.py` or `python3 sendmail.py` depending on what you want to do.

In case it isn't already obvious, don't do this over a repeater or during a net because people will hate you.

## Still to do

* Make it remember your callsign

* Contacts list?

* Integrate it with Thunderbird

* GUI or TUI

* Selective Email Reception (Only showing emails addressed to your callsign)

* SnackMail email address that forwards emails from ham radio to internet (would require a base station connected to a computer that is always on).

* Play image attachments using SSTV?

Email me (ilan@snackmail.cc) if you have any ideas.

