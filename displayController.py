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
SCR_ROT = const(1)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)



fonts = [glcdfont,tt14,tt24]

class Message:
    def __init__(self,msg,username):
        self.msg = msg
        self.username = username

class DisplayController:
    spi = SPI(
            0,
            baudrate=40000000,
            miso=Pin(MISO),
            mosi=Pin(MOSI),
            sck=Pin(CLK))
    
    display = ILI9341(
            spi,
            cs=Pin(13),
            dc=Pin(DC),
            rst=Pin(RST),
            w=SCR_WIDTH,
            h=SCR_HEIGHT,
            r=SCR_ROT)
    
    queue = []
    
    def __init__(self):
        self.display.erase()
        self.display.set_pos(0,0)
        self.display.set_font(fonts[2])
        self.display.print("Messages empty")
    
    def refresh(self):
        self.display.erase()
        self.display.set_pos(0,0)
        for msg in self.queue:
            self.display.write(msg.username+": "+msg.msg+"\n")
    
    def add_message(self,msg,username):
        if len(self.queue) >= 3:
            self.queue.pop(0)
        
        self.queue.append(Message(msg[:100],username[:16]))
        self.refresh()