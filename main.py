import time

import pyautogui as gui
from pyjoycon import ButtonEventJoyCon, get_R_id, get_L_id

POLL_RATE = 1/2000 # in s, ie 1/Hz
MOUSE_SPEED = 100000 # in px/s
SCROLL_SPEED = 10000
INVERT_SCROLL = 1

joyconR = ButtonEventJoyCon(*get_R_id())
joyconL = ButtonEventJoyCon(*get_L_id())

MODE = "mouse" # "mouse" or "keyboard"
FAST_MODE = False
joyconR.home_led_on()

# Features:
#   - Switch between mouse or keyboard mode by pressing the home button. Home button light is on if in mouse mode
#   When in mouse mode:
#       - Move cursor with left stick
#       - Scroll with right stick
#       - Can speed up mouse cursor by holding down the ZR button
#       - Left click with A
#       - Right click with X
#       - Double click with B

def rumble(device):
    device._RUMBLE_DATA = b"\x05\x10\x10\x05\x05\x10\x10\x05"
    device._write_output_report(b'\x10', b'', b'')

while 1:
    for event_type, status in joyconL.events():
        pass
        #print("L", event_type, status)
        #rumble(joyconL)
    for event_type, status in joyconR.events():
        # switch modes
        if event_type == "home" and status == 1:
            MODE = "mouse" if MODE == "keyboard" else "keyboard"
            rumble(joyconR)
            if MODE == "mouse":
                joyconR.home_led_on()
            else:
                joyconR.home_led_off()
        
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
        print(event_type, status)

    L_status = joyconL.get_status()
    x = L_status['analog-sticks']['left']['horizontal']
    y = -L_status['analog-sticks']['left']['vertical']
    multiplier = 1. if FAST_MODE else 0.25
    if x != 0 or y != 0:
        gui.moveRel(x * multiplier * MOUSE_SPEED * POLL_RATE, y * multiplier * MOUSE_SPEED * POLL_RATE)

    R_status = joyconR.get_status()
    y = INVERT_SCROLL * R_status['analog-sticks']['right']['vertical']
    if y != 0:
        gui.scroll(y * multiplier * SCROLL_SPEED * POLL_RATE)

    time.sleep(POLL_RATE)