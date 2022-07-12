from machine import SPI, Pin

from ili934xnew import ILI9341, color565
from micropython import const
import os
import glcdfont
import tt14
import tt24
#import tt32

CLK = const(6)
MOSI = const(7)
MISO = const(4)
DC = const(15)
RST = const(14)

SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

# PROBABLY NEED TO PACK ALL THIS INTO A CLASS

fonts = [glcdfont,tt14,tt24]
text = 'Hello Raspberry Pi Pico/ili9341'

#print(text)


spi = SPI(
    0,
    baudrate=40000000,
    miso=Pin(MISO),
    mosi=Pin(MOSI),
    sck=Pin(CLK))
print(spi)

display = ILI9341(
    spi,
    cs=Pin(13),
    dc=Pin(DC),
    rst=Pin(RST),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

display.erase()
display.set_pos(0,0)


for ff in fonts:
    display.set_font(ff)
    display.print(text)
    sleep(1)