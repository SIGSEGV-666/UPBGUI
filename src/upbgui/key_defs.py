AKEY = 'a'
BKEY = 'b'
CKEY = 'c'
DKEY = 'd'
EKEY = 'e'
FKEY = 'f'
GKEY = 'g'
HKEY = 'h'
IKEY = 'i'
JKEY = 'j'
KKEY = 'k'
LKEY = 'l'
MKEY = 'm'
NKEY = 'n'
OKEY = 'o'
PKEY = 'p'
QKEY = 'q'
RKEY = 'r'
SKEY = 's'
TKEY = 't'
UKEY = 'u'
VKEY = 'v'
WKEY = 'w'
XKEY = 'x'
YKEY = 'y'
ZKEY = 'z'

ZEROKEY = '0'
ONEKEY = '1'
TWOKEY = '2'
THREEKEY = '3'
FOURKEY = '4'
FIVEKEY = '5'
SIXKEY = '6'
SEVENKEY = '7'
EIGHTKEY = '8'
NINEKEY = '9'

CAPSLOCKKEY = 211

LEFTCTRLKEY = 212
LEFTALTKEY = 213
RIGHTALTKEY = 214
RIGHTCTRLKEY = 215
RIGHTSHIFTKEY = 216
LEFTSHIFTKEY = 217

ESCKEY = 218
TABKEY = 219
RETKEY = ENTERKEY = 220
SPACEKEY = 221
LINEFEEDKEY = 222
BACKSPACEKEY = 223
DELKEY = 224
SEMICOLONKEY = 225
PERIODKEY = 226
COMMAKEY = 227
QUOTEKEY = 228
ACCENTGRAVEKEY = 229
MINUSKEY = 230
SLASHKEY = 232
BACKSLASHKEY = 233
EQUALKEY = 234
LEFTBRACKETKEY = 235
RIGHTBRACKETKEY = 236

LEFTARROWKEY = 137
DOWNARROWKEY = 138
RIGHTARROWKEY = 139
UPARROWKEY = 140

PAD0 = 150
PAD1 = 151
PAD2 = 152
PAD3 = 153
PAD4 = 154
PAD5 = 155
PAD6 = 156
PAD7 = 157
PAD8 = 158
PAD9 = 159


PADPERIOD = 199
PADSLASHKEY = 161
PADASTERKEY = 160

PADMINUS = 162
PADENTER = 163
PADPLUSKEY = 164

F1KEY = 300
F2KEY = 301
F3KEY = 302
F4KEY = 303
F5KEY = 304
F6KEY = 305
F7KEY = 306
F8KEY = 307
F9KEY = 308
F10KEY = 309
F11KEY = 310
F12KEY = 311
F13KEY = 312
F14KEY = 313
F15KEY = 314
F16KEY = 315
F17KEY = 316
F18KEY = 317
F19KEY = 318

PAUSEKEY = 165
INSERTKEY = 166
HOMEKEY = 167
PAGEUPKEY = 168
PAGEDOWNKEY = 169
ENDKEY = 170

OSKEY = 172
def key_to_char(key, is_shifted):
        char = None
        key = (ord(key) if not isinstance(key, int) else key)
        if ord(AKEY) <= key <= ord(ZKEY):
                if is_shifted: char = chr(key - 32)
                else: char = chr(key)

        elif ord(ZEROKEY) <= key <= ord(NINEKEY):
                if not is_shifted: char = chr(key)
                else:
                        key = chr(key)
                        if key == ZEROKEY: char = ")"
                        elif key == ONEKEY: char = "!"
                        elif key == TWOKEY: char = "@"
                        elif key == THREEKEY: char = "#"
                        elif key == FOURKEY: char = "$"
                        elif key == FIVEKEY: char = "%"
                        elif key == SIXKEY: char = "^"
                        elif key == SEVENKEY: char = "&"
                        elif key == EIGHTKEY: char = "*"
                        elif key == NINEKEY: char = "("

        elif PAD0 <= key <= PAD9:
                char = str(key - PAD0)
        elif key == PADPERIOD: char = "."
        elif key == PADSLASHKEY: char = "/"
        elif key == PADASTERKEY: char = "*"
        elif key == PADMINUS: char = "-"
        elif key == PADPLUSKEY: char = "+"
        elif key == SPACEKEY: char = " "
        elif key == TABKEY: char = "\t"
        elif key in (ENTERKEY, PADENTER):
                char = "\n"
        elif not is_shifted:
                if key == ACCENTGRAVEKEY: char = "`"
                elif key == MINUSKEY: char = "-"
                elif key == EQUALKEY: char = "="
                elif key == LEFTBRACKETKEY: char = "["
                elif key == RIGHTBRACKETKEY: char = "]"
                elif key == BACKSLASHKEY: char = "\\"
                elif key == SEMICOLONKEY: char = ";"
                elif key == QUOTEKEY: char = "'"
                elif key == COMMAKEY: char = ","
                elif key == PERIODKEY: char = "."
                elif key == SLASHKEY: char = "/"
        else:
                if key == ACCENTGRAVEKEY: char = "~"
                elif key == MINUSKEY: char = "_"
                elif key == EQUALKEY: char = "+"
                elif key == LEFTBRACKETKEY: char = "{"
                elif key == RIGHTBRACKETKEY: char = "}"
                elif key == BACKSLASHKEY: char = "|"
                elif key == SEMICOLONKEY: char = ":"
                elif key == QUOTEKEY: char = '"'
                elif key == COMMAKEY: char = "<"
                elif key == PERIODKEY: char = ">"
                elif key == SLASHKEY: char = "?"
        return char
