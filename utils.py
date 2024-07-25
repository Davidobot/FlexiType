import pygame
from pygame._sdl2.video import Window

def rumble(device):
    device._RUMBLE_DATA = b"\x05\x10\x10\x05\x05\x10\x10\x05"
    device._write_output_report(b'\x10', b'', b'')

def show_window(WINDOW_SIZE, desktop_w, desktop_h ):
    background_colour = (0, 0, 0) 
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.NOFRAME) 
    screen.fill(background_colour) 

    window = Window.from_display_module()
    window.position = ((desktop_w - WINDOW_SIZE)/2, desktop_h-WINDOW_SIZE)

    pygame.display.flip() 
    return screen

def hide_window():
    screen = pygame.display.set_mode((1, 1),  pygame.HIDDEN) 
    pygame.display.flip() 
    return screen

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

PETAL_COORDS = [(120,0), (240,0), (240,120), (240,240), (120,240), (0,240), (0,120), (0,0)]

#XYBA
TXTSIZE = 32
BUTTONS = [0, 3, 2, 1]
COLORS = [BLUE, YELLOW, RED, GREEN]
COORDS = [(0, TXTSIZE), (TXTSIZE, 0), (TXTSIZE * 2, TXTSIZE), (TXTSIZE, TXTSIZE * 2)]
BASE_SET = ['abcd', 'efgh', 'ijkl', 'mnop', 'qrst', 'uvwx', 'yz,.', ':/@-']
CAPS_SET = ['ABCD', 'EFGH', 'IJKL', 'MNOP', 'QRST', 'UVWX', 'YZ?!', ';\\&_']
NUMS_SET = ['1234', '5678', '90*+', 'xx$`', '\'"~|', '=#%^', '<>[]', '{}()']

def getPetalSurf(petalString, TXTFONT, colors=False):
    petalSurf = pygame.surface.Surface((TXTSIZE * 3, TXTSIZE * 3)) # A square
    for i in range(4):
        if colors == False:
            petalSurf.blit(TXTFONT.render(petalString[i], True, WHITE), COORDS[i])
        elif colors == True:
            petalSurf.blit(TXTFONT.render(petalString[i], True, COLORS[i]), COORDS[i])

    return petalSurf