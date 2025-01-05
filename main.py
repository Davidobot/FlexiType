import time, math

import pygame

import pyautogui as gui
from pyjoycon import ButtonEventJoyCon, get_R_id, get_L_id
import sys

from utils import *

FPS = 1000 # in frames per second
MOUSE_SPEED = 800 # in px/s
SCROLL_SPEED = 100 # in px/s
INVERT_SCROLL = 1 # direction of scrolling
WINDOW_SIZE = 264 # in px

# Features:
#   - Switch between mouse or keyboard mode by pressing the home button. Home button light is on if in mouse mode
#   When in mouse mode:
#       - Move cursor with left stick
#       - Scroll with right stick
#       - Can speed up mouse cursor by holding down the ZR button
#       - Left click with A
#       - Right click with X
#       - Double click with B
#   When in keyboard mode:
#       - Hold ZL (numbers) or ZR (caps) to switch keyboard set
#       - Move left stick to select 'petal' then press the corresponding ABXY button on the right joycon to type
#       
#

joyconR_connected, joyconL_connected = get_R_id() != (None, None, None), get_L_id() != (None, None, None)

if not joyconR_connected and not joyconL_connected:
    gui.alert("Please restart the program after you connect both joycons.")
    sys.exit()
if not joyconR_connected or not joyconL_connected:
    left_or_right = "right" if not joyconR_connected else "left"
    gui.alert(f"Please restart the program after you connect the {left_or_right} joycon.")
    sys.exit()

SHOW_INSTRUCTIONS = False
if SHOW_INSTRUCTIONS:
    gui.alert("""-- FlexiType --
    Features:
    - Switch between mouse or keyboard mode by pressing the HOME button. Home button light is on if in mouse mode
        a. When in mouse mode:
        - Move cursor with left stick
        - Scroll with right stick
        - Can speed up mouse cursor by holding down the ZR button
        - Left click with A
        - Right click with X
        - Double click with B
        b. When in keyboard mode:
        - Hold ZL (numbers) or ZR (caps) to switch keyboard set
        - Move left stick to select 'petal' then press the corresponding ABXY button on the right joycon to type""")

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
SMALL_TXTFONT = pygame.font.Font(None, SMALL_TXTSIZE)
TXTFONT.set_bold(True)
SMALL_TXTFONT.set_bold(True)

MODE = "mouse" # "mouse" or "keyboard"
FAST_MODE = False
pygame.init()

# icon = pygame.image.load('icon.png') 
# pygame.display.set_icon(icon)

_infoObject = pygame.display.Info()
desktop_w, desktop_h = _infoObject.current_w, _infoObject.current_h
mouse_mode() if MODE == "mouse" else keyboard_mode()

buttons_index = {'x': 1, 'a': 2, 'b': 3, 'y': 0}
extras = [['delete', 'backspace', 'space', 'return'],
        ['left', 'up', 'right', 'down'],
        ['f1', 'f2', 'f3', 'f4']]
clock = pygame.time.Clock()
running = True
PREV_PETAL = -1
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            running = False

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
        selectedExtraSet = 0
        #Determine where the stick's pointing and which petal to select.  -1 means no petal is selected.
        L_status = joyconL.get_status(); R_status = joyconR.get_status()
        xPos = L_status['analog-sticks']['left']['horizontal']
        yPos = -L_status['analog-sticks']['left']['vertical']

        # switch keyboard set
        if R_status['buttons']['right']['zr'] and not L_status['buttons']['left']['zl']:
            selectedSet = CAPS_SET
            selectedExtraSet = 2
        if L_status['buttons']['left']['zl'] and not R_status['buttons']['right']['zr']:
            selectedSet = NUMS_SET
            selectedExtraSet = 1
        if not L_status['buttons']['left']['zl'] and not R_status['buttons']['right']['zr']:
            selectedSet = BASE_SET
            selectedExtraSet = 0

        petal = -1
        angle = math.atan2(yPos,xPos)
        mag = math.dist((0, 0), (xPos, yPos))
        angle = angle if angle > 0 else (2*math.pi + angle)
        angle = (angle + math.pi/4 - 3*math.pi/2) % (math.pi * 2)
        
        if mag > 0.75:
            petal = math.floor(angle / (math.pi/4))

        if PREV_PETAL != petal:
            rumble(joyconL)
        PREV_PETAL = petal

        #Blit and schtuff
        for i in range(8):
            colors = False
            if i == petal:
                colors = True

            petalSurf = getPetalSurf(selectedSet[i], TXTFONT, colors)
            screen.blit(petalSurf, PETAL_COORDS[i])
        extraSurf = getExtraSurf(EXTRA_SET[selectedExtraSet], SMALL_TXTFONT, petal == -1)
        screen.blit(extraSurf, (100, 100))

        pygame.display.flip()

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
        else:
            if event_type in buttons_index.keys() and petal != -1 and status == 0:
                i = buttons_index[event_type]
                gui.press(selectedSet[petal][i])
            if event_type in buttons_index.keys() and petal == -1 and status == 0:
                i = buttons_index[event_type]
                gui.press(extras[selectedExtraSet][i])