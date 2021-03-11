import smbus
import time
import configparser
import os
import mojimoji

LCD_CHR = 1
LCD_CMD = 0 

LCD_LINE = [0x80, 0xC0, 0x94, 0xD4]
LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0 
LCD_LINE_3 = 0x94 
LCD_LINE_4 = 0xD4 

ENABLE = 0b00000100

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1)
class HD44780(object):
    def __init__(self, configfile):
        """Initialize the LCD.

        Parameters
        ----------
        configfile : str
            lcd config file name
            Create config file under the conf folder
        """
        dirname = os.path.dirname( os.path.abspath( __file__ ) )

        self._configfile = dirname + '/conf/' + configfile
        self.loadconfig()
        self._shift = True 
        self._shiftlen = 0
        self._length = [0, 0, 0, 0]

    def init(self):
        self.lcd_byte(0x33,LCD_CMD)
        self.lcd_byte(0x32,LCD_CMD)
        self.lcd_byte(0x06,LCD_CMD)
        self.lcd_byte(0x0C,LCD_CMD)
        self.lcd_byte(0x28,LCD_CMD)
        self.lcd_byte(0x01,LCD_CMD)
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | self._backlight
        bits_low = mode | ((bits<<4) & 0xF0) | self._backlight
        bus.write_byte(self._i2caddr, bits_high)
        self.lcd_toggle_enable(bits_high)
        bus.write_byte(self._i2caddr, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self,bits):
        time.sleep(E_DELAY)
        bus.write_byte(self._i2caddr, (bits | ENABLE))
        time.sleep(E_PULSE)
        bus.write_byte(self._i2caddr, (bits & ~ENABLE))
        time.sleep(E_DELAY)

    def lcd_string(self, message, line):
        self.lcd_byte(line, LCD_CMD)
        for i in range(len(message)):
            self.lcd_byte(ord(message[i]),LCD_CHR)

    def set_lcd_i2caddress(self, i2caddr):
        self._i2caddr(i2caddr)

    def lshift(self):
        self.lcd_byte(0x18, LCD_CMD)

    def rshift(self):
        self.lcd_byte(0x1C, LCD_CMD)

    def message(self, message, lineno, readconfig=True):
        if readconfig:
            self.loadconfig()

        if self._kanamode:
            message = mojimoji.zen_to_han(message,\
                                          kana=True,\
                                          digit=True,\
                                          ascii=True)
            self._length[lineno - 1] = len(message)
            message = mojimoji.han_to_zen(message,\
                                          kana=True,\
                                          digit=False,\
                                          ascii=False)

            self.lcd_string_kana(message, LCD_LINE[lineno - 1])

        else:
            self._length[lineno - 1] = len(message)

            self.lcd_string(message, LCD_LINE[lineno - 1])

        if (self._shiftmode != 0) and \
           ((max(self._length) - self._width) > 0) and \
           (self._length.index(max(self._length)) == (lineno - 1)):

            self.shiftcontroll(max(self._length))

    def setbacklight(self, backlight=True):
        if backlight:
            self._backlight = 0x08
        else:
            self._backlight = 0x00

        self.lcd_byte(0x00 ,LCD_CMD)

    def shiftcontroll(self, messagelength):
        if self._shiftmode == 1:
            self.lshift()
        elif self._shiftmode == 2:
            self.rshift()
        elif self._shiftmode == 3:

            excesslen = messagelength - self._width
            if excesslen > 0:
                if ((excesslen - self._shiftlen) > 0) and self._shift:
                    self.lshift()
                    self._shiftlen += 1
                    if self._shiftlen == excesslen:
                        self._shift = False
                        self._shiftlen = 0
                else:
                    self.rshift()
                    self._shiftlen += 1
                    if self._shiftlen == excesslen:
                        self._shift = True
                        self._shiftlen = 0

    def loadconfig(self):
        config = configparser.ConfigParser()
        config.read( self._configfile )
        self._i2caddr       = int(config.get('lcd', 'i2c_address'), 0)
        self._width         = config.getint('lcd', 'width')
        self._lines         = config.getint('lcd', 'lines')
        self._backlightflag = config.getboolean('lcd', 'backlight')
        self._shiftmode     = config.getint('lcd', 'shiftmode')
        self._kanamode      = config.getboolean('lcd', 'kanamode')

        self.setbacklight(self._backlightflag)

    def getwidth(self):
        return self._width

    def str2bool(self, boolstring):
        return boolstring.lower() in ("yes", "true", "on", "1", "t")

    def lcd_string_kana(self, message, line):
        codes = u'線線線線線線線線線線線線線線線線　　　　　　　　　　'\
                u'　　　　　　　!"#$%&()*+,-./0123456789:;<=>?@ABCDEFG'\
                u'HIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{'\
                u'|}→←　　　　　　　　　　　　　　　　　　　　　　　　'\
                u'　　　　　　　　　。「」、・ヲァィゥェォャュョッーア'\
                u'イウエオカキクケコサシスセソタチツテトナニヌネノハヒ'\
                u'フヘホマミムメモヤユヨラリルレロワン゛゜αäβεμσρq√陰ι'\
                u'×￠￡nöpqθ∞ΩüΣπxν千万円÷　塗'
        dic ={u'ガ':u'カ゛',u'ギ':u'キ゛',u'グ':u'ク゛',\
                u'ゲ':u'ケ゛',u'ゴ':u'コ゛',u'ザ':u'サ゛',\
                u'ジ':u'シ゛',u'ズ':u'ス゛',u'ゼ':u'セ゛',\
                u'ゾ':u'ソ゛',u'ダ':u'タ゛',u'ヂ':u'チ゛',\
                u'ヅ':u'ツ゛',u'デ':u'テ゛',u'ド':u'ト゛',\
                u'バ':u'ハ゛',u'ビ':u'ヒ゛',u'ブ':u'フ゛',\
                u'ベ':u'ヘ゛',u'ボ':u'ホ゛',u'パ':u'ハ゜',\
                u'ピ':u'ヒ゜',u'プ':u'フ゜',u'ペ':u'ヘ゜',\
                u'ポ':u'ホ゜',u'℃':u'゜C'}

        self.lcd_byte(line, LCD_CMD)
        message2 = ''
        for i in range(len(message)):
            if (message[i] in dic.keys()):
                message2 += dic[message[i]]
            else:
                message2 += message[i]

        for i in range(len(message2)):
            if message2[i] == ' ':
                self.lcd_byte(ord(message2[i]), LCD_CHR)
            elif (codes.find(message2[i]) >= 0):
                self.lcd_byte(codes.find(message2[i]) + 1, LCD_CHR)
            elif (codes_han.find(message2[i]) >= 0):
                self.lcd_byte(codes.find(message2[i]) + 1, LCD_CHR)
            elif (message2[i] != u' '):
                self.lcd_byte('?', LCD_CHR)