MARK_CODE = '1'
SPACE_CODE = '0'

START_BIT = MARK_CODE + SPACE_CODE
STOP_BIT = MARK_CODE

#__wrap:Callable[[str],str] = lambda symb: START_BIT + symb + STOP_BIT
__wrap = lambda symb: START_BIT + symb + STOP_BIT

# Baudot code (simplified example mapping)
BAUDOT:dict[str, str|dict[str,str]] = {
        'letters': {
                'A': __wrap('11000'), 'B': __wrap('10011'), 'C' : __wrap('01110'), 'D' : __wrap('10010'), 'E': __wrap('10000'),
                'F': __wrap('10110'), 'G': __wrap('01011'), 'H' : __wrap('00101'), 'I' : __wrap('01100'), 'J': __wrap('11010'),
                'K': __wrap('11110'), 'L': __wrap('01001'), 'M' : __wrap('00111'), 'N' : __wrap('00110'), 'O': __wrap('00011'),
                'P': __wrap('01101'), 'Q': __wrap('11101'), 'R' : __wrap('01010'), 'S' : __wrap('10100'), 'T': __wrap('00001'),
                'U': __wrap('11100'), 'V': __wrap('01111'), 'W' : __wrap('11001'), 'X' : __wrap('10111'), 'Y': __wrap('10101'),
                'Z': __wrap('10001'), ' ': __wrap('00100'), '\n': __wrap('00010'), '\r': __wrap('00000')
        },
        'figures': {
                '1': __wrap('11101'), '2' : __wrap('11001'), '3': __wrap('10000'), '4': __wrap('01010'), '5': __wrap('00001'),
                '6': __wrap('10101'), '7' : __wrap('11100'), '8': __wrap('01100'), '9': __wrap('00011'), '0': __wrap('01101'),
                '-': __wrap('11000'), '\'': __wrap('11010'), '!': __wrap('10110'), '&': __wrap('01011'), '#': __wrap('00101'),
                '(': __wrap('11110'), ')' : __wrap('01001'), '"': __wrap('10001'), '/': __wrap('10111'), ':': __wrap('01110'),
                ';': __wrap('01111'), '?' : __wrap('10011'), ',': __wrap('00110'), '.': __wrap('00111'), '$': __wrap('10010'), 
                ' ': __wrap('00100'), '`' : __wrap('11010'),
        },
        'LTRS': __wrap('11111'),  # Letters shift
        'FIGS': __wrap('11011')   # Figures shift
}

mode = 0  # 0=letters, 1=figures

def decode_baudot(five_bits):
	global mode
	code = ''.join(str(b) for b in five_bits)
	if code == '11111':  # LTRS
		mode = 0
		return ''
	if code == '11011':  # FIGS
		mode = 1
		return ''
#	table = BAUDOT_LETTERS if mode == 0 else BAUDOT_FIGURES
#	return table.get(code, '')
	mode_name = 'letters' if mode == 0 else 'figures'
	for char, wrapped in BAUDOT[mode_name].items():
		if wrapped[2:7] == code:
			return char
	return ''
