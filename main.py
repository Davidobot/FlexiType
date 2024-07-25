import time

import pygame

import pyautogui as gui
from pyjoycon import ButtonEventJoyCon, get_R_id, get_L_id

from utils import *

FPS = 1000 # in frames per second
MOUSE_SPEED = 800 # in px/s
SCROLL_SPEED = 100 # in px/s
INVERT_SCROLL = 1 # direction of scrolling
WINDOW_SIZE = 360 # in px

# Features:
#   - Switch between mouse or keyboard mode by pressing the home button. Home button light is on if in mouse mode
#   When in mouse mode:
#       - Move cursor with left stick
#       - Scroll with right stick
#       - Can speed up mouse cursor by holding down the ZR button
#       - Left click with A
#       - Right click with X
#       - Double click with B

joyconR = ButtonEventJoyCon(*get_R_id())
joyconL = ButtonEventJoyCon(*get_L_id())
global screen
def mouse_mode():
    global screen
    joyconR.home_led_on()
    screen = hide_window()

def keyboard_mode():
    global screen
    joyconR.home_led_off()
    screen = show_window(WINDOW_SIZE, desktop_w, desktop_h)

pygame.font.init()
TXTFONT = pygame.font.Font(None, TXTSIZE)
TXTFONT.set_bold(True)

MODE = "mouse" # "mouse" or "keyboard"
FAST_MODE = False
pygame.init()
_infoObject = pygame.display.Info()
desktop_w, desktop_h = _infoObject.current_w, _infoObject.current_h
mouse_mode() if MODE == "mouse" else keyboard_mode()

clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            running = False

    for event_type, status in joyconL.events():
        pass
        #print("L", event_type, status)
        #rumble(joyconL)
    for event_type, status in joyconR.events():
        # switch modes
        if event_type == "home" and status == 1:
            MODE = "mouse" if MODE == "keyboard" else "keyboard"
            rumble(joyconR)
            mouse_mode() if MODE == "mouse" else keyboard_mode()
        
        # things in mouse mode
        if MODE == "mouse":
            if event_type == "zr":
                FAST_MODE = True if status == 1 else False
            if event_type == "a":
                if status == 1:
                    gui.mouseDown()
                else:
                    gui.mouseUp()
            if event_type == "x" and status == 1:
                gui.rightClick()
            if event_type == "b" and status == 1:
                gui.doubleClick()

    if MODE == "mouse":
        L_status = joyconL.get_status()
        x = L_status['analog-sticks']['left']['horizontal']
        y = -L_status['analog-sticks']['left']['vertical']
        multiplier = 1. if FAST_MODE else 0.25
        if x != 0 or y != 0:
            gui.moveRel(int(x * multiplier * MOUSE_SPEED * dt), int(y * multiplier * MOUSE_SPEED * dt))

        R_status = joyconR.get_status()
        y = INVERT_SCROLL * R_status['analog-sticks']['right']['vertical']
        if y != 0:
            gui.scroll(int(y * multiplier * SCROLL_SPEED * dt))
    else:
        screen.fill((0,0,0))
        selectedSet = BASE_SET
        #Determine where the stick's pointing and which petal to select.  -1 means no petal is selected.
        xPos = 0 #gamepad.get_axis(0)
        yPos = 0 #gamepad.get_axis(1)

        petal = -1
        if xPos >= .75:
            if yPos >= .75:
                petal = 3
            elif yPos <= -.75:
                petal = 1
            else:
                petal = 2

        elif xPos <= -.75:
            if yPos >= .75:
                petal = 5
            elif yPos <= -.75:
                petal = 7
            else:
                petal = 6

        else:
            if yPos >= .75:
                petal = 4
            elif yPos <= -.75:
                petal = 0

        # if facePress and petal != -1:
        #     for i in range(4):
        #         if BUTTONS[i] == faceButton:
        #            kbEmu.tap_key(selectedSet[petal][i])
        #Blit and schtuff
        for i in range(8):
            colors = False
            if i == petal:
                colors = True

            petalSurf = getPetalSurf(selectedSet[i], TXTFONT, colors)
            screen.blit(petalSurf, PETAL_COORDS[i])

        pygame.display.update()