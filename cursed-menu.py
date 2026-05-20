import curses
import local_libraries.sendmail_library as sendmail
sendmail.init()

menu = ['Inbox', 'Send', 'Monitor', 'Settings', 'Exit']

def inbox(stdscr):
	stdscr.clear()
	stdscr.addstr(0,0, "RTTY Email Client > Inbox", curses.A_REVERSE)
	stdscr.addstr(15, 30, "aaaa")
	stdscr.refresh()
	stdscr.getch()  # each this call just waits for you to press any key

def print_menu(stdscr, selected):
	stdscr.clear()
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
	stdscr.noutrefresh()

def send(stdscr):
	stdscr.clear()
	stdscr.addstr(0,0, "RTTY Email Client > Send", curses.A_REVERSE)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
	BLUE_BLACK = curses.color_pair(1)
	stdscr.addstr(1, 0, 'test', BLUE_BLACK | curses.A_BOLD)
	stdscr.refresh()
	emails = sendmail.create()
	stdscr.addstr(10,10, str(emails))
	stdscr.getch()
def monitor(stdscr):
	stdscr.clear()
	stdscr.addstr(0,0, "RTTY Email Client > Monitor", curses.A_REVERSE)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
	BLUE_BLACK = curses.color_pair(1)
	stdscr.addstr(1, 0, 'test', BLUE_BLACK | curses.A_BOLD)
	stdscr.refresh()
	emails = "To be added"
	stdscr.addstr(10,10, str(emails))
	stdscr.getch()
def settings(stdscr):
	stdscr.clear()
	stdscr.addstr(0,0, "RTTY Email Client > Settings", curses.A_REVERSE)
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
	RED_WHITE = curses.color_pair(1)
	stdscr.addstr(1, 0, 'test')
	stdscr.refresh()
	stdscr.getch()

def main(stdscr):
	height, width = stdscr.getmaxyx()
	curses.curs_set(0)
	current_row = 0
	print_menu(stdscr, current_row)
	curses.doupdate()
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
		print_menu(stdscr, current_row)
		curses.doupdate()
curses.wrapper(main)
