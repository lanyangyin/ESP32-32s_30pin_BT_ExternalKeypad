"""
The MIT License (MIT)
Copyright © 2020 Walkline Wang (https://walkline.wang)
https://gitee.com/walkline/esp32-ble
"""


from micropython import const


class KeyCode(object):
    # 7	Keyboard
    KC_NONE = const(0x00)  # 保留（无事件指示）
    # 0x01	键盘翻转错误
    # 0x02	键盘POST失败
    # 0x03	键盘错误未定义

    KC_A = const(0x04)  # Keyboard a and A
    KC_B = const(0x05)  # Keyboard b and B
    KC_C = const(0x06)  # Keyboard c and C
    KC_D = const(0x07)  # Keyboard d and D
    KC_E = const(0x08)  # Keyboard e and E
    KC_F = const(0x09)  # Keyboard f and F
    KC_G = const(0x0A)  # Keyboard g and G
    KC_H = const(0x0B)  # Keyboard h and H
    KC_I = const(0x0C)  # Keyboard i and I
    KC_J = const(0x0D)  # Keyboard j and J
    KC_K = const(0x0E)  # Keyboard k and K
    KC_L = const(0x0F)  # Keyboard l and L
    KC_M = const(0x10)  # Keyboard m and M
    KC_N = const(0x11)  # Keyboard n and N
    KC_O = const(0x12)  # Keyboard o and O
    KC_P = const(0x13)  # Keyboard p and P
    KC_Q = const(0x14)  # Keyboard q and Q
    KC_R = const(0x15)  # Keyboard r and R
    KC_S = const(0x16)  # Keyboard s and S
    KC_T = const(0x17)  # Keyboard t and T
    KC_U = const(0x18)  # Keyboard u and U
    KC_V = const(0x19)  # Keyboard v and V
    KC_W = const(0x1A)  # Keyboard w and W
    KC_X = const(0x1B)  # Keyboard x and X
    KC_Y = const(0x1C)  # Keyboard y and Y
    KC_Z = const(0x1D)  # Keyboard z and Z

    KC_1 = const(0x1E)  # 1 and !
    KC_2 = const(0x1F)  # 2 and @
    KC_3 = const(0x20)  # 3 and #
    KC_4 = const(0x21)  # 4 and $
    KC_5 = const(0x22)  # 5 and %
    KC_6 = const(0x23)  # 6 and ^
    KC_7 = const(0x24)  # 7 and &
    KC_8 = const(0x25)  # 8 and *
    KC_9 = const(0x26)  # 9 and (
    KC_0 = const(0x27)  # 0 and )

    KC_ENTER = KC_ENT = const(0x28)  # Return (Enter)
    KC_ESCAPE = KC_ESC = const(0x29)  # Escape
    KC_BSPACE = KC_BSPC = const(0x2A)  # Delete (Backspace)
    KC_TAB = const(0x2B)  # Tab
    KC_SPACE = KC_SPC = const(0x2C)  # Spacebar
    KC_MINUS = KC_MINS = const(0x2D)  # - and _
    KC_EQUAL = KC_EQL = const(0x2E)  # = and +
    KC_LBRACKET = KC_LBRC = const(0x2F)  # [ and {
    KC_RBRACKET = KC_RBRC = const(0x30)  # ] and }
    KC_BSLASH = KC_BSLS = const(0x31)  # \ and |
    KC_NONUS_HASH = KC_NUHS = const(0x32)  # Non-US # and ~
    KC_SCOLON = KC_SCLN = const(0x33)  # ; and :
    KC_QUOTE = KC_QUOT = const(0x34)  # ' and "
    KC_GRAVE = KC_GRV = KC_ZKHK = const(0x35)  # ` and ~, JIS Zenkaku/Hankaku
    KC_COMMA = KC_COMM = const(0x36)  # , and <
    KC_DOT = const(0x37)  # . and >
    KC_SLASH = KC_SLSH = const(0x38)  # / and ?
    KC_CAPSLOCK = KC_CLCK = KC_CAPS = const(0x39)  # Caps Lock

    KC_F1 = const(0x3A)  # Keyboard F1
    KC_F2 = const(0x3B)  # Keyboard F2
    KC_F3 = const(0x3C)  # Keyboard F3
    KC_F4 = const(0x3D)  # Keyboard F4
    KC_F5 = const(0x3E)  # Keyboard F5
    KC_F6 = const(0x3F)  # Keyboard F6
    KC_F7 = const(0x40)  # Keyboard F7
    KC_F8 = const(0x41)  # Keyboard F8
    KC_F9 = const(0x42)  # Keyboard F9
    KC_F10 = const(0x43)  # Keyboard F10
    KC_F11 = const(0x44)  # Keyboard F11
    KC_F12 = const(0x45)  # Keyboard F12
    KC_F13 = const(0x68)  # Keyboard F13
    KC_F14 = const(0x69)  # Keyboard F14
    KC_F15 = const(0x6A)  # Keyboard F15
    KC_F16 = const(0x6B)  # Keyboard F16
    KC_F17 = const(0x6C)  # Keyboard F17
    KC_F18 = const(0x6D)  # Keyboard F18
    KC_F19 = const(0x6E)  # Keyboard F19
    KC_F20 = const(0x6F)  # Keyboard F20
    KC_F21 = const(0x70)  # Keyboard F21
    KC_F22 = const(0x71)  # Keyboard F22
    KC_F23 = const(0x72)  # Keyboard F23
    KC_F24 = const(0x73)  # Keyboard F24

    KC_PSCREEN = KC_PSCR = const(0x46)  # Print Screen
    KC_SCROLLLOCK = KC_SLCK = KC_BRMD = const(0x47)  # Scroll Lock, Brightness Down (macOS)
    KC_PAUSE = KC_PAUS = KC_BRK = KC_BRMU = const(0x48)  # Pause, Brightness Up (macOS)
    KC_INSERT = KC_INS = const(0x49)  # Insert
    KC_HOME = const(0x4A)  # Home
    KC_PGUP = const(0x4B)  # Page Up
    KC_DELETE = KC_DEL = const(0x4C)  # Forward Delete
    KC_END = const(0x4D)  # End
    KC_PGDOWN = KC_PGDN = const(0x4E)  # Page Down

    KC_RIGHT = KC_RGHT = const(0x4F)  # Right Arrow
    KC_LEFT = const(0x50)  # Left Arrow
    KC_DOWN = const(0x51)  # Down Arrow
    KC_UP = const(0x52)  # Up Arrow

    KC_NUMLOCK = KC_NLCK = const(0x53)  # Keypad Num Lock and Clear
    KC_KP_SLASH = KC_PSLS = const(0x54)  # Keypad /
    KC_KP_ASTERISK = KC_PAST = const(0x55)  # Keypad *
    KC_KP_MINUS = KC_PMNS = const(0x56)  # Keypad -
    KC_KP_PLUS = KC_PPLS = const(0x57)  # Keypad +
    KC_KP_ENTER = KC_PENT = const(0x58)  # Keypad ENTER
    KC_KP_1 = KC_P1 = const(0x59)  # Keypad 1 and End
    KC_KP_2 = KC_P2 = const(0x5A)  # Keypad 2 and Down Arrow
    KC_KP_3 = KC_P3 = const(0x5B)  # Keypad 3 and Page Down
    KC_KP_4 = KC_P4 = const(0x5C)  # Keypad 4 and Left Arrow
    KC_KP_5 = KC_P5 = const(0x5D)  # Keypad 5
    KC_KP_6 = KC_P6 = const(0x5E)  # Keypad 6 and Right Arrow
    KC_KP_7 = KC_P7 = const(0x5F)  # Keypad 7 and Home
    KC_KP_8 = KC_P8 = const(0x60)  # Keypad 8 and Up Arrow
    KC_KP_9 = KC_P9 = const(0x61)  # Keypad 9 and Page Up
    KC_KP_0 = KC_P0 = const(0x62)  # Keypad 0 and Insert
    KC_KP_DOT = KC_PDOT = const(0x63)  # Keypad . and Delete
    KC_NONUS_BSLASH = KC_NUBS = const(0x64)  # Non-US \ and |
    KC_KP_EQUAL = KC_PEQL = const(0x67)  # Keypad =
    KC_KP_COMMA = KC_PCMM = const(0x85)  # Keypad ,
    KC_KP_EQUAL_AS400 = const(0x86)  # Keypad = on AS/400 keyboards

    KC_APPLICATION = KC_APP = const(0x65)  # Application (Windows Menu Key)
    KC_POWER = const(0x66)  # System Power (macOS)
    KC_EXECUTE = KC_EXEC = const(0x74)  # Execute
    KC_HELP = const(0x75)  # Help
    KC_MENU = const(0x76)  # Menu
    KC_SELECT = KC_SLCT = const(0x77)  # Select
    KC_STOP = const(0x78)  # Stop
    KC_AGAIN = KC_AGIN = const(0x79)  # Again
    KC_UNDO = const(0x7A)  # Undo
    KC_CUT = const(0x7B)  # Cut
    KC_COPY = const(0x7C)  # Copy
    KC_PASTE = KC_PSTE = const(0x7D)  # Paste
    KC_FIND = const(0x7E)  # Find
    KC_MUTE = const(0x7F)  # Mute (macOS)
    KC_VOLUP = const(0x80)  # Volume Up (macOS)
    KC_VOLDOWN = const(0x81)  # Volume Down (macOS)
    KC_LOCKING_CAPS = KC_LCAP = const(0x82)  # Locking Caps Lock
    KC_LOCKING_NUM = KC_LNUM = const(0x83)  # Locking Num Lock
    KC_LOCKING_SCROLL = KC_LSCR = const(0x84)  # Locking Scroll Lock

    KC_INT1 = KC_RO = const(0x87)  # JIS \ and _
    KC_INT2 = KC_KANA = const(0x88)  # JIS Katakana/Hiragana
    KC_INT3 = KC_JYEN = const(0x89)  # JIS ¥ and |
    KC_INT4 = KC_HENK = const(0x8A)  # JIS Henkan
    KC_INT5 = KC_MHEN = const(0x8B)  # JIS Muhenkan
    KC_INT6 = const(0x8C)  # JIS Numpad ,
    KC_INT7 = const(0x8D)  # International 7
    KC_INT8 = const(0x8E)  # International 8
    KC_INT9 = const(0x8F)  # International 9

    KC_LANG1 = KC_HAEN = const(0x90)  # Hangul/English
    KC_LANG2 = KC_HANJ = const(0x91)  # Hanja
    KC_LANG3 = const(0x92)  # JIS Katakana
    KC_LANG4 = const(0x93)  # JIS Hiragana
    KC_LANG5 = const(0x94)  # JIS Zenkaku/Hankaku
    KC_LANG6 = const(0x95)  # Language 6
    KC_LANG7 = const(0x96)  # Language 7
    KC_LANG8 = const(0x97)  # Language 8
    KC_LANG9 = const(0x98)  # Language 9

    KC_ALT_ERASE = KC_ERAS = const(0x99)  # Alternate Erase
    KC_SYSREQ = const(0x9A)  # SysReq/Attention
    KC_CANCEL = const(0x9B)  # Cancel
    KC_CLEAR = KC_CLR = const(0x9C)  # Clear
    KC_PRIOR = const(0x9D)  # Prior
    KC_RETURN = const(0x9E)  # Return
    KC_SEPARATOR = const(0x9F)  # Separator
    KC_OUT = const(0xA0)  # Out
    KC_OPER = const(0xA1)  # Oper
    KC_CLEAR_AGAIN = const(0xA2)  # Clear/Again
    KC_CRSEL = const(0xA3)  # CrSel/Props
    KC_EXSEL = const(0xA4)  # ExSel

    KC_LCTRL = KC_LCTL = const(0xE0)  # Left Control
    KC_LSHIFT = KC_LSFT = const(0xE1)  # Left Shift
    KC_LALT = const(0xE2)  # Left Alt
    KC_LGUI = KC_LCMD = KC_LWIN = const(0xE3)  # Left GUI (Windows/Command/Meta key)
    KC_RCTRL = KC_RCTL = const(0xE4)  # Right Control
    KC_RSHIFT = KC_RSFT = const(0xE5)  # Right Shift
    KC_RALT = KC_ALGR = const(0xE6)  # Right Alt (AltGr)
    KC_RGUI = KC_RCMD = KC_RWIN = const(0xE7)  # Right GUI (Windows/Command/Meta key)

    # 自定义控制键
    KC_CONTROL_FN = KCC_FN = const(0xff00)
    KC_CONTROL_NONE = KCC_NONE = const(0xff01)
    KC_CONTROL_NUMBER = KCC_NUM = const(0xff02)
    KC_CONTROL_MEDIA = KCC_MEDIA = const(0xff03)
    KC_CONTROL_MOUSE = KCC_MOSUE = const(0xff04)
    KC_CONTROL_SETTINGS = KCC_SET = const(0xff05)
    KC_CONTROL_TEST = KCC_TEST = const(0xff06)
    # KC_CONTROL_LIGHT = KCC_LIGHT = const(0xff07)
    # KC_CONTROL_BRIGHT_UP = KCC_BUP = const(0xff08)
    # KC_CONTROL_BRIGHT_DOWN = KCC_BDOWN = const(0xff09)
