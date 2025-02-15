import pygame
from pygame._sdl2.video import Window
import sys
import os

def rumble(device):
    device._RUMBLE_DATA = b"\x05\x10\x10\x05\x05\x10\x10\x05"
    device._write_output_report(b'\x10', b'', b'')

def show_window(WINDOW_SIZE, desktop_w, desktop_h ):
    pygame.display.quit()
    background_colour = (0, 0, 0) 
    pygame.display.set_caption('FlexiType')
    if getattr(sys, 'frozen', False):
        icon = pygame.image.load(os.path.join(sys._MEIPASS, 'icons/flexitype-icon.png'))
    else:
        icon = pygame.image.load('icons/flexitype-icon.png') 
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.NOFRAME) 
    screen.fill(background_colour) 

    window = Window.from_display_module()
    window.position = ((desktop_w - WINDOW_SIZE)/2, desktop_h-WINDOW_SIZE*1.4)

    pygame.display.flip() 
    return screen

def hide_window():
    pygame.display.quit()
    if getattr(sys, 'frozen', False):
        icon = pygame.image.load(os.path.join(sys._MEIPASS, 'icons/flexitype-icon.png'))
    else:
        icon = pygame.image.load('icons/flexitype-icon.png') 
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((10, 10),  pygame.HIDDEN) 
    pygame.display.flip() 
    return screen

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

PETAL_COORDS = [(100,0), (200,0), (200,100), (200,200), (100,200), (0,200), (0,100), (0,0)]

#XYBA
TXTSIZE = 24
SMALL_TXTSIZE = 16
BUTTONS = [0, 3, 2, 1]
COLORS = [BLUE, YELLOW, RED, GREEN]
COORDS = [(0, TXTSIZE), (TXTSIZE, 0), (TXTSIZE * 2, TXTSIZE), (TXTSIZE, TXTSIZE * 2)]
BS = TXTSIZE * 3
SMALL_COORDS = [(0, (BS - SMALL_TXTSIZE)/2), ((BS - 3*SMALL_TXTSIZE)/2, 0), (BS - 3*SMALL_TXTSIZE, (BS - SMALL_TXTSIZE)/2), ((BS - 3*SMALL_TXTSIZE)/2, BS - SMALL_TXTSIZE)]
BASE_SET = ['abcd', 'efgh', 'ijkl', 'mnop', 'qrst', 'uvwx', 'yz,.', ':/@-']
CAPS_SET = ['ABCD', 'EFGH', 'IJKL', 'MNOP', 'QRST', 'UVWX', 'YZ?!', ';\\&_']
NUMS_SET = ['1234', '5678', '90*+', 'xx$`', '\'"~|', '=#%^', '<>[]', '{}()']
EXTRA_SET = [['DEL', 'RET', 'SPC', 'BCK'], ['<--', '^^^', '-->', 'DWN'], ['F1', 'F2', 'F3', 'F4']]

def getPetalSurf(petalString, TXTFONT, colors=False):
    petalSurf = pygame.surface.Surface((TXTSIZE * 3, TXTSIZE * 3)) # A square
    for i in range(4):
        if colors == False:
            petalSurf.blit(TXTFONT.render(petalString[i], True, WHITE), COORDS[i])
        elif colors == True:
            petalSurf.blit(TXTFONT.render(petalString[i], True, COLORS[i]), COORDS[i])

    return petalSurf

def getExtraSurf(petalString, TXTFONT, colors=False):
    petalSurf = pygame.surface.Surface((TXTSIZE * 3, TXTSIZE * 3)) # A square
    for i in range(4):
        if colors == False:
            petalSurf.blit(TXTFONT.render(petalString[i], True, WHITE), SMALL_COORDS[i])
        elif colors == True:
            petalSurf.blit(TXTFONT.render(petalString[i], True, COLORS[i]), SMALL_COORDS[i])

    return petalSurf