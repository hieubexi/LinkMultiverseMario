import pygame
from pygame.locals import *

__calls_down_event = {}
__calls_up_event = {}
__mouse_down_event = {}
__mouse_up_event = {}


# ==== Mouse input ==== #

def handle_mouse_input(game_event: pygame.event):
    if not (game_event.type == MOUSEBUTTONDOWN
            or game_event.type == MOUSEBUTTONDOWN):
        return

    button = button_to_str(game_event.button)

    if game_event.type == MOUSEBUTTONDOWN:
        __notify_mouse_button_down(button)
    elif game_event.type == MOUSEBUTTONUP:
        __notify_mouse_button_up(button)


def button_to_str(button: int) -> str:
    if button == 1:
        return "left"
    elif button == 2:
        return "middle"
    elif button == 3:
        return "right"


def add_mouse_button_down_event(key: str, function):
    if key in __calls_down_event:
        __calls_down_event[key].append(function)
    else:
        __calls_down_event[key] = [function]


def add_mouse_button_up_event(key: str, function):
    if key in __calls_up_event:
        __calls_up_event[key].append(function)
    else:
        __calls_up_event[key] = [function]


def remove_mouse_button_down_event(button: str, function):
    __mouse_down_event[button].remove(function)


def remove_mouse_button_up_event(button: str, function):
    __mouse_down_event[button].remove(function)


def __notify_mouse_button_down(button: str):
    if button not in __mouse_down_event:
        return
    for f in __mouse_down_event[button]:
        f()


def __notify_mouse_button_up(button: str):
    if button not in __mouse_up_event:
        return
    for f in __mouse_up_event[button]:
        f()


# ==== Keyboard input ==== #

def handle_keyboard_input(game_event: pygame.event):
    if not (game_event.type == KEYDOWN or game_event.type == KEYUP):
        return
    key = key_to_str(game_event.key)
    if game_event.type == KEYDOWN:
        __notify_key_down(key)
    elif game_event.type == KEYUP:
        __notify_key_up(key)


def key_to_str(key: int) -> str:
    if 33 <= key <= 126:
        return chr(key)
    elif key == 32:
        return "space"
    elif key == 1073742050:
        return "alt"
    elif key == 1073742048:
        return "ctrl"
    elif key == 1073742049 or key == 1073742053:
        return "shift"
    elif key == 1073741881:
        return "caps"
    elif key == 27:
        return "esc"
    elif key == 9:
        return "tab"
    elif key == 1073741904:
        return "left"
    elif key == 1073741906:
        return "up"
    elif key == 1073741903:
        return "right"
    elif key == 1073741905:
        return "down"
    elif key == 13:
        return "return"
    return "other"


def add_key_down_event(key: str, function):
    if key in __calls_down_event:
        __calls_down_event[key].append(function)
    else:
        __calls_down_event[key] = [function]


def add_key_up_event(key: str, function):
    if key in __calls_up_event:
        __calls_up_event[key].append(function)
    else:
        __calls_up_event[key] = [function]


def remove_key_down_event(key: str, function):
    __calls_down_event[key].remove(function)


def remove_key_up_event(key: str, function):
    __calls_up_event[key].remove(function)


def __notify_key_down(key: str):
    if key not in __calls_down_event:
        return
    for f in __calls_down_event[key]:
        f()


def __notify_key_up(key: str):
    if key not in __calls_up_event:
        return
    for f in __calls_up_event[key]:
        f()
