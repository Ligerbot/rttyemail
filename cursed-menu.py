import email
import time
import curses
import curses.textpad
import local_libraries.sendmail_library as sendmail
import local_libraries.recieve as recieve
recieve.init()
sendmail.init()

menu = ['Inbox', 'Send', 'Monitor', 'Settings', 'Exit']

def inbox(stdscr):
	stdscr.clear()
	stdscr.addstr(0,0, "RTTY Email Client > Inbox", curses.A_REVERSE)
	stdscr.addstr(15, 30, "aaaa")
	stdscr.refresh()
	stdscr.getch()  # each this call just waits for you to press any key
	stdscr.clear()
def print_menu(stdscr, selected, mainscreen, menu):
#	stdscr.clear()
	stdscr.refresh()
	if mainscreen:
		stdscr.addstr(0,0, "RTTY Email Client", curses.A_REVERSE)
	height, width = stdscr.getmaxyx()
	for idx, row in enumerate(menu):
		x = width // 2 - len(row) // 2
		y = height // 2 - len(menu) // 2 + idx
		if idx == selected:
			stdscr.attron(curses.A_REVERSE)
			stdscr.addstr(y, x, row)
			stdscr.attroff(curses.A_REVERSE)
		else:
			stdscr.addstr(y, x, row)
		stdscr.refresh()
	stdscr.noutrefresh()
	stdscr.refresh()
def send(stdscr):
	stdscr.clear()
	stdscr.addstr(0,0, "RTTY Email Client > Send", curses.A_REVERSE)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
	BLUE_BLACK = curses.color_pair(1)
#	stdscr.addstr(1, 0, 'test', BLUE_BLACK | curses.A_BOLD)
	curses.textpad.rectangle(stdscr, 1, 0, 25, 55)
	stdscr.addstr(3,6, "To: ")
	curses.textpad.rectangle(stdscr, 2, 10, 4, 21)
	stdscr.addstr(6,1, "Subject: ")
	curses.textpad.rectangle(stdscr, 5, 10, 7, 36)
#	stdscr.addstr(12,0, "Body: ")
	curses.textpad.rectangle(stdscr, 8, 1, 23, 51)
#	stdscr.border(19, 30, 19, 30, 20, 30, 30, 30)
#	textboxobj = curses.textpad.Textbox(stdscr).edit()
#	test = textboxobj.gather()
#	stdscr.addstr(20, 20, test)
	stdscr.refresh()
	to = curses.newwin(1, 9, 3, 12)
	subject = curses.newwin(1, 25, 6, 11)
	body = curses.newwin(14, 49, 9, 2)
	box = curses.textpad.Textbox(to)
	curses.curs_set(1)
	box.edit()
	toField = box.gather()
	stdscr.refresh()
	box = curses.textpad.Textbox(subject)
	box.edit()
	subjectField = box.gather()
	stdscr.refresh()
	box = curses.textpad.Textbox(body)
	stdscr.addstr(24,1,"* CTRL + g to finish typing")
	stdscr.refresh()
	box.edit()
	bodyField = box.gather()
	curses.curs_set(0)
#	stdscr.addstr(40,30,toField.strip())
#	stdscr.addstr(41,30,subjectField.strip())
#	stdscr.addstr(42,30,bodyField.strip())
	emails = sendmail.create(toField, subjectField, bodyField)
	sendmenu = ["Send (audio)", "Print Email Text", "Cancel"]
	current_row = 0
	stdscr.keypad(True)
	print_menu(stdscr, current_row, False, sendmenu)
	show = False
	while True:
		key = stdscr.getch()
		if key == curses.KEY_UP and current_row > 0:
			current_row -= 1
		elif key == curses.KEY_DOWN and current_row < len(sendmenu) - 1:
			current_row += 1
		elif key == curses.KEY_ENTER or key in [10, 13]:
			if current_row == 0:
				stdscr.clear()
				stdscr.addstr(0,0,"RTTY Email Client > Send > Waiting To Send", curses.A_REVERSE)
				stdscr.addstr(2,0,"Press enter to send the email")
#				stdscr.addstr(3,0,emails.decode("utf-8", errors="replace"))
				if show:
					stdscr.addstr(3,0,emails.decode("utf-8", errors="replace"))
				while True:
					key = stdscr.getch()
					if key == curses.KEY_ENTER or key in [10, 13]:
						stdscr.addstr(0,0,"RTTY Email Client > Send > Sending In Progress...", curses.A_REVERSE)
						stdscr.addstr(1,0,"Sending in progress, don't exit the program until finished...")
						stdscr.refresh()
						sendmail.transmit(emails)
						stdscr.addstr(1,0,"Sending Finished                                             ")
						stdscr.refresh()
						break
				time.sleep(0.7)
				break
			if current_row == 1:
				show = True
				stdscr.clear()
				stdscr.addstr(0,0,"RTTY Email Client > Send > View Email", curses.A_REVERSE)
				stdscr.addstr(3,0,emails.decode("utf-8", errors="replace"))
			if current_row == 2:
				break
		print_menu(stdscr, current_row, False, sendmenu)
		stdscr.refresh()

#	stdscr.addstr(40,0,emails.decode("utf-8", errors="replace"))
	stdscr.refresh()
#	stdscr.getch()
	stdscr.clear()
def monitor(stdscr):
	output = ""
	stdscr.clear()
	stdscr.addstr(0,0, "RTTY Email Client > Monitor", curses.A_REVERSE)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
	BLUE_BLACK = curses.color_pair(1)
#	stdscr.addstr(1, 0, 'test', BLUE_BLACK | curses.A_BOLD)
	stdscr.refresh()
	height, width = stdscr.getmaxyx()
#	emails = [
#		"test 1",
#		"test 2",
#		"test3",
#		"test 4"
#	]
	emails = ["Start Monitoring", "Exit"]
	selected = 0
	while True:
		centerX = width // 2
		centerY = height // 2
		i = 0
		stdscr.addstr(4, centerX - 26, "                        Press Start to Listen                           ")
		stdscr.refresh()
#		output = recieve.listenforemail(stdscr)
#		stdscr.addstr(0,3,str(output))
#		msg = email.message_from_string(output)
		for THISemail in emails:
			if i == selected:
				stdscr.addstr(5 + i, centerX, THISemail, curses.A_REVERSE)
			else:
				stdscr.addstr(5 + i,centerX,THISemail, curses.COLOR_BLUE)
			stdscr.refresh()
			i = i + 1
		key = stdscr.getch()
		if key == curses.KEY_DOWN and selected < len(emails) - 1:
			selected = selected + 1
		if key == curses.KEY_UP and selected > 0:
			selected = selected - 1
#		stdscr.addstr(1,0,"Debug: " + str(selected) + str(len(emails)))
#		stdscr.refresh()
		if key == curses.KEY_ENTER or key in [10, 13]:
			if selected == len(emails) - 1:
				stdscr.addstr(1,0,"Exiting, one second...")
				stdscr.refresh()
				#exit(0)
				break
			if selected == 0:
				stdscr.addstr(4, centerX - 25, "Listening for any emails (freezes screen until one is recieved)")
				stdscr.refresh()
				output = recieve.listenforemail(stdscr)
				if output != None:
					output = output.replace("---START RTTY EMAIL---", "")
					output = output.replace("---END RTTY EMAIL---", "")
					msg = email.message_from_string(output.strip())
#				emails.insert(1, str(str(msg['From']) + " - " + str(msg['Subject'])))
				if msg['From'] == None or msg['Subject'] == None:
					emails.insert(1, str("Unable To Decode" + " - " + "Too Many Errors"))
				else:
					emails.insert(1, str(str(msg['From']) + " - " + str(msg['Subject'])))
#				stdscr.addstr(2,0,"Recieved: " + str(output))
				stdscr.refresh()
			else:
				stdscr.clear()
				stdscr.addstr(0,0,"RTTY Email Client > Monitor > Email Reader", curses.A_REVERSE)
				reader = curses.newwin(25, 60, centerY - 12, centerX-30)
				reader.box()
#				curses.textpad.rectangle(reader,0,0,28,28)
				reader.addstr(2, 2, output)
				stdscr.refresh()
				reader.refresh()
				while True:
					key = reader.getch()
					if key == ord("q") or key == 27 or key in [10, 13]:
						break
				del reader

		if output == "user-exit":
			stdscr.addstr(1,0,"Exiting, one second...")
			stdscr.refresh()
			break
#			while True:
#				stdscr.addstr(


#	stdscr.getch()
	stdscr.clear()
def settings(stdscr):
	stdscr.clear()
	stdscr.addstr(0,0, "RTTY Email Client > Settings", curses.A_REVERSE)
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
	RED_WHITE = curses.color_pair(1)
	stdscr.addstr(2,0, "Callsign: ")
	curses.textpad.rectangle(stdscr, 1, 10, 3, 23)
	stdscr.refresh()
	callsign = curses.newwin(1, 12, 2, 11)
	box = curses.textpad.Textbox(callsign)
	curses.curs_set(1)
	box.edit()
	newcallsign = box.gather()

#	stdscr.addstr(1, 0, 'test')
	stdscr.refresh()
	stdscr.getch()
	stdscr.clear()
def main(stdscr):
	height, width = stdscr.getmaxyx()
	curses.curs_set(0)
	current_row = 0
	print_menu(stdscr, current_row, True, menu)
	curses.doupdate()
#	stdscr.clear()
	while True:
		key = stdscr.getch()
		if key == curses.KEY_UP and current_row > 0:
			current_row -= 1
		elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
			current_row += 1
		elif key == curses.KEY_ENTER or key in [10, 13]:
			if current_row == 0:
				inbox(stdscr)
			if current_row == 1:
				send(stdscr)
			if current_row == 2:
				monitor(stdscr)
			if current_row == 3:
				settings(stdscr)
			if current_row == len(menu) - 1:
				break
		print_menu(stdscr, current_row, True, menu)
		curses.doupdate()
curses.wrapper(main)
